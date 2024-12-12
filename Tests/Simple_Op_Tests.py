"""
Simple operator tests
"""


def test_addition(calc_handler):
    result, error_list = calc_handler.run_single_exp("3+5")
    assert error_list is None
    assert result == 8


def test_subtraction(calc_handler):
    result, error_list = calc_handler.run_single_exp("10-2")
    assert error_list is None
    assert result == 8


def test_multiplication(calc_handler):
    result, error_list = calc_handler.run_single_exp("4*3")
    assert error_list is None
    assert result == 12


def test_division(calc_handler):
    result, error_list = calc_handler.run_single_exp("12/4")
    assert error_list is None
    assert result == 3


def test_power(calc_handler):
    result, error_list = calc_handler.run_single_exp("2^3")
    assert error_list is None
    assert result == 8


def test_modulo(calc_handler):
    result, error_list = calc_handler.run_single_exp("10%3")
    assert error_list is None
    assert result == 1


def test_max(calc_handler):
    result, error_list = calc_handler.run_single_exp("6$9")
    assert error_list is None
    assert result == 9


def test_min(calc_handler):
    result, error_list = calc_handler.run_single_exp("4&2")
    assert error_list is None
    assert result == 2


def test_avg(calc_handler):
    result, error_list = calc_handler.run_single_exp("4@2")
    assert error_list is None
    assert result == 3


def test_factorial(calc_handler):
    result, error_list = calc_handler.run_single_exp("4!")
    assert error_list is None
    assert result == 24


def test_negative_op(calc_handler):
    result, error_list = calc_handler.run_single_exp("~5")
    assert error_list is None
    assert result == -5


def test_hash_op(calc_handler):
    result, error_list = calc_handler.run_single_exp("123#")
    assert error_list is None
    assert result == 6


def test_unary_minus(calc_handler):
    # U-5 = -5
    result, error_list = calc_handler.run_single_exp("1+-5")
    assert error_list is None
    assert result == -4


def test_power_neg(calc_handler):
    result, error_list = calc_handler.run_single_exp("2^-2")
    assert error_list is None
    assert result == 0.25


def test_hash_again(calc_handler):
    result, error_list = calc_handler.run_single_exp("-9999##")
    assert error_list is None
    assert result == -9
