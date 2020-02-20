import pytest
import logging
logger = logging.getLogger('test')


@pytest.fixture(params=[0, 1], ids=['cat', 'dog'])
def prepare(request):
    return request.param


def my_func(a):
    logger.error("some error")
    return a + 1


def test_caplog_fixture(caplog):
    caplog.set_level(logging.ERROR)
    assert my_func(3) == 3


@pytest.mark.parametrize("test_input", [1, 2, 3])
def test_my_func_2(prepare, test_input):
    logger.info(f"Prepare value = {prepare}")
    logger.info(f"Input value = {test_input}")
    assert 0 == 1


