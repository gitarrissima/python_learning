import pytest
import os
import sys


cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(cur_dir)
import helpers


@pytest.mark.parametrize("account, expected_code, expected_response",
                         [
                             ('valid', 200, {'score': 0.5}),
                             ('', 200, {'score': 0.5}),
                             (1, 422, "Parameter 'account' expected to be string. Actual type is <class 'int'>")
                         ])
def test_account_field(api_connection, account, expected_code, expected_response):
    request = {"account": account, "login": "login", "method": "online_score",
               "arguments": {"first_name": "first", "last_name": "last"}}
    helpers.set_valid_auth(request)
    actual_response, actual_code = api_connection.get_response(request)
    assert actual_code == expected_code
    assert actual_response == expected_response


@pytest.mark.parametrize("login, expected_code, expected_response",
                         [
                             ('valid', 200, {'score': 0.5}),
                             ('', 200, {'score': 0.5}),
                             (1, 422, "Parameter 'login' expected to be string. Actual type is <class 'int'>")
                         ])
def test_login_field(api_connection, login, expected_code, expected_response):
    request = {"account": "account", "login": login, "method": "online_score",
               "arguments": {"first_name": "first", "last_name": "last"}}
    helpers.set_valid_auth(request)
    actual_response, actual_code = api_connection.get_response(request)
    assert actual_code == expected_code
    assert actual_response == expected_response


@pytest.mark.parametrize("method, expected_code, expected_response",
                         [
                             ('', 422, "Error: Parameter 'method' should not be empty"),
                             (1, 422, "Parameter 'method' expected to be string. Actual type is <class 'int'>")
                         ])
def test_method_field(api_connection, method, expected_code, expected_response):
    request = {"account": "account", "login": "login", "method": method,
               "arguments": {"first_name": "first", "last_name": "last"}}
    helpers.set_valid_auth(request)
    actual_response, actual_code = api_connection.get_response(request)
    assert actual_code == expected_code
    assert actual_response in expected_response


@pytest.mark.parametrize("token, expected_code, expected_response",
                         [
                             ('', 403, {'error': 'Forbidden'}),
                             (1, 422, "Parameter 'token' expected to be string. Actual type is <class 'int'>")
                         ])
def test_token_field(api_connection, token, expected_code, expected_response):
    request = {"account": "account", "login": "login", "method": "online_score", "token": token,
               "arguments": {"first_name": "first", "last_name": "last"}}
    actual_response, actual_code = api_connection.get_response(request)
    assert actual_code == expected_code
    assert actual_response == expected_response


@pytest.mark.parametrize("arguments, expected_code, expected_response",
                         [
                             ({}, 422,
                              "At least one pair should be not None: phone-email, first_name-last_name, gender-birthday"),
                             (1, 422, "Parameter 'arguments' expected to be dict. Actual type is <class 'int'>")
                         ])
def test_arguments_field(api_connection, arguments, expected_code, expected_response):
    request = {"account": "account", "login": "login", "method": "online_score",
               "arguments": arguments}
    helpers.set_valid_auth(request)
    actual_response, actual_code = api_connection.get_response(request)
    assert actual_code == expected_code
    assert actual_response == expected_response


@pytest.mark.parametrize("phone, expected_code, expected_response",
                         [
                             ('80009998888', 422,
                              "Parameter 'phone' should contain 11 numeric symbols and start with '7'. Actual length is 11, first symbol is 8"),
                             ('+70009998888', 422,
                              "Parameter 'phone' should contain 11 numeric symbols and start with '7'. Actual length is 12, first symbol is +"),
                             (1, 422,
                              "Parameter 'phone' should contain 11 numeric symbols and start with '7'. Actual length is 1, first symbol is 1"),
                             (70009998888, 200, {'score': 0.5})
                         ])
def test_phone_field(api_connection, phone, expected_code, expected_response):
    request = {"account": "account", "login": "login", "method": "online_score",
               "arguments": {"first_name": "first", "last_name": "last", "phone": phone}}
    helpers.set_valid_auth(request)
    actual_response, actual_code = api_connection.get_response(request)
    assert actual_code == expected_code
    assert actual_response == expected_response


@pytest.mark.parametrize("email, expected_code, expected_response",
                         [
                             ('test', 422, "Parameter 'email' should contain '@'"),
                             ('test@', 422, "Parameter 'email' contains invalid domain part: ''"),
                             (1, 422, "Parameter 'email' should be 'str'. Actual type is <class 'int'>"),
                             ('', 422, "Parameter 'email' should contain '@'")
                         ])
def test_email_field(api_connection, email, expected_code, expected_response):
    request = {"account": "account", "login": "login", "method": "online_score",
               "arguments": {"first_name": "first", "last_name": "last", "email": email}}
    helpers.set_valid_auth(request)
    actual_response, actual_code = api_connection.get_response(request)
    assert actual_code == expected_code
    assert actual_response == expected_response


@pytest.mark.parametrize("first_name, expected_code, expected_response",
                         [
                             ('valid', 200, {'score': 0.5}),
                             ('', 200, {'score': 0.5}),
                             (1, 422, "Parameter 'first_name' expected to be string. Actual type is <class 'int'>")
                         ])
def test_first_name_field(api_connection, first_name, expected_code, expected_response):
    request = {"account": "account", "login": "login", "method": "online_score",
               "arguments": {"first_name": first_name, "last_name": "last"}}
    helpers.set_valid_auth(request)
    actual_response, actual_code = api_connection.get_response(request)
    assert actual_code == expected_code
    assert actual_response == expected_response


@pytest.mark.parametrize("last_name, expected_code, expected_response",
                         [
                             ('valid', 200, {'score': 0.5}),
                             ('', 200, {'score': 0.5}),
                             (1, 422, "Parameter 'last_name' expected to be string. Actual type is <class 'int'>")
                         ])
def test_last_name_field(api_connection, last_name, expected_code, expected_response):
    request = {"account": "account", "login": "login", "method": "online_score",
               "arguments": {"first_name": "first_name", "last_name": last_name}}
    helpers.set_valid_auth(request)
    actual_response, actual_code = api_connection.get_response(request)
    assert actual_code == expected_code
    assert actual_response == expected_response


@pytest.mark.parametrize("birthday, expected_code, expected_response",
                         [
                             ('11.12.2000', 200, {'score': 0.5}),
                             ('1.1.1900', 422, "Parameter 'birthday' provided expected to be less than 70 years ago"),
                             ('', 200, {'score': 0.5}),
                             (1, 422, "Failed to convert value '1' to date. Expected format: 'DD.MM.YYYY'")
                         ])
def test_birthday_field(api_connection, birthday, expected_code, expected_response):
    request = {"account": "account", "login": "login", "method": "online_score",
               "arguments": {"first_name": "first_name", "last_name": "last_name", "birthday": birthday}}
    helpers.set_valid_auth(request)
    actual_response, actual_code = api_connection.get_response(request)
    assert actual_code == expected_code
    assert actual_response == expected_response


@pytest.mark.parametrize("gender, expected_code, expected_response",
                         [
                             (0, 200, {'score': 0.5}),
                             (1, 200, {'score': 0.5}),
                             (2, 200, {'score': 0.5}),
                             (3, 422, "Parameter 'gender' expected to be in set (0, 1, 2)"),
                             ('0', 422, "Parameter 'gender' should be 'int'. Actual type is <class 'str'>")
                         ])
def test_gender_field(api_connection, gender, expected_code, expected_response):
    request = {"account": "account", "login": "login", "method": "online_score",
               "arguments": {"first_name": "first_name", "last_name": "last_name", "gender": gender}}
    helpers.set_valid_auth(request)
    actual_response, actual_code = api_connection.get_response(request)
    assert actual_code == expected_code
    assert actual_response == expected_response


@pytest.mark.parametrize("client_ids, expected_code, expected_response",
                         [
                             ([0], 200, ""),
                             ([0, 1], 200, ""),
                             (0, 422, "Parameter 'client_ids' should be 'list'. Actual type is <class 'int'>"),
                             ('string', 422, "Parameter 'client_ids' should be 'list'. Actual type is <class 'str'>"),
                             (['0', '1'], 422,
                              "Parameter 'client_ids' should contain only 'int' elements, but it contains '0', which type is <class 'str'>")
                         ])
def test_client_ids_field(api_connection, client_ids, expected_code, expected_response):
    request = {"account": "account", "login": "login", "method": "clients_interests",
               "arguments": {"client_ids": client_ids}}
    helpers.set_valid_auth(request)
    actual_response, actual_code = api_connection.get_response(request)
    assert actual_code == expected_code
    if actual_code == 200:
        for client_id in client_ids:
            assert client_id in actual_response
    else:
        assert actual_response == expected_response


@pytest.mark.parametrize("date, expected_code, expected_response",
                         [
                             ('11.12.2000', 200, ""),
                             ('1.1.1900', 200, ""),
                             ('0.32.2000', 422,
                              "Failed to convert value '0.32.2000' to date. Expected format: 'DD.MM.YYYY'"),
                             ('', 200, ""),
                             (1, 422, "Failed to convert value '1' to date. Expected format: 'DD.MM.YYYY'")
                         ])
def test_date_field(api_connection, date, expected_code, expected_response):
    request = {"account": "account", "login": "login", "method": "clients_interests",
               "arguments": {"client_ids": [0, 1], "date": date}}
    helpers.set_valid_auth(request)
    actual_response, actual_code = api_connection.get_response(request)
    assert actual_code == expected_code
    if actual_code == 200:
        assert 0 in actual_response
        assert 1 in actual_response
    else:
        assert actual_response == expected_response
