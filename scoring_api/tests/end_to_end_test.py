import pytest
import requests
import json
import os
import sys

cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(cur_dir)
import helpers


def test_base_requests_invalid(end_to_end_setup):
    payload = {"bad_format": "very_bad"}
    helpers.set_valid_auth(payload)
    response = requests.post('http://localhost:8001/method', json=payload, stream=True)
    resp_content = json.loads(response.content)
    assert response.status_code == 422
    assert resp_content['code'] == 422
    assert "Required parameter 'login' should be defined" in resp_content['error']


@pytest.mark.parametrize("payload, status_code, content",
                         [
                             ({"phone": "74951234567", "email": "test"}, 422, "Parameter 'email' should contain '@'"),
                             ({"first_name": "d", "last_name": "e"}, 200, {'score': 0.5})
                         ])
def test_online_score(end_to_end_setup, payload, status_code, content):
    request = {"account": "account1", "login": "login1", "method": "online_score", "arguments": payload}
    helpers.set_valid_auth(request)
    response = requests.post('http://localhost:8001/method', json=request)
    resp_content = json.loads(response.content)
    assert response.status_code == status_code
    assert resp_content['code'] == status_code
    if status_code == 200:
        assert resp_content['response'] == content
    else:
        assert content in resp_content['error']


@pytest.mark.parametrize("payload, status_code, content",
                         [
                             ({"date": "20.07.2017"}, 422, "Required parameter 'client_ids' should be defined"),
                             ({"client_ids": [1, 2], "date": "19.07.2017"}, 200, "")
                         ])
def test_clients_interests(end_to_end_setup, payload, status_code, content):
    request = {"account": "account1", "login": "login1", "method": "clients_interests", "arguments": payload}
    helpers.set_valid_auth(request)
    response = requests.post('http://localhost:8001/method', json=request)
    resp_content = json.loads(response.content)
    assert response.status_code == status_code
    assert resp_content['code'] == status_code
    if status_code == 200:
        for client_id in payload['client_ids']:
            key = str(client_id)
            assert key in resp_content['response']
            assert isinstance(resp_content['response'][key], list)
    else:
        assert content in resp_content['error']


def test_invalid_token(end_to_end_setup):
    request = {"account": "account1", "login": "login1", "token": "invalid_token", "method": "online_score",
               "arguments": {"first_name": "d", "last_name": "e"}}
    response = requests.post('http://localhost:8001/method', json=request)
    resp_content = json.loads(response.content)
    assert response.status_code == 403
    assert resp_content['code'] == 403
    assert resp_content['error'] == {'error': 'Forbidden'}
