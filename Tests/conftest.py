import pytest
from CalcHandler import CalcHandler

@pytest.fixture
def calc_handler():
    return CalcHandler()