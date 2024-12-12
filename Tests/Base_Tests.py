"""
Simple syntax tests along with 1 gibberish 1 empty 1 whitespace test
"""


def test_1(calc_handler):
    result, error_list = calc_handler.run_single_exp("2*^3")
    assert result is None
    assert error_list[0].get_msg() == "Missing operands for: * at position: 1"


def test_2(calc_handler):
    result, error_list = calc_handler.run_single_exp("2*")
    assert result is None
    assert error_list[0].get_msg() == "Invalid Operator usage: * ,at position: 1"


def test_3(calc_handler):
    result, error_list = calc_handler.run_single_exp("(+)")
    assert result is None
    assert error_list[0].get_msg() == "Missing operands for: + at position: 1"


def test_4(calc_handler):
    result, error_list = calc_handler.run_single_exp("(2+2")
    assert result is None
    assert error_list[0].get_msg() == "Missing Closing parentheses to opening parentheses at position: 0"


def test_5(calc_handler):
    result, error_list = calc_handler.run_single_exp("~(2*3)")
    assert result is None
    assert error_list[0].get_msg() == "Invalid use of ~ at position: 0"


def test_6(calc_handler):
    result, error_list = calc_handler.run_single_exp("asdasdasdasgLDLA")
    assert result is None
    assert error_list[0].get_msg() == "Invalid Chars found: asdasdasdasgLDLA ,at position: 0 -> 15"


def test_7(calc_handler):
    result, error_list = calc_handler.run_single_exp("")
    assert result is None
    assert error_list[0].get_msg() == "Invalid Input, The input must contain an expression"


def test_8(calc_handler):
    result, error_list = calc_handler.run_single_exp("1                 +               2")
    assert error_list is None
    assert result == 3
