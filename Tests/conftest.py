import pytest
from CalcHandler import CalcHandler


@pytest.fixture
def calc_handler():
    # fixture used in all the tests
    return CalcHandler()
