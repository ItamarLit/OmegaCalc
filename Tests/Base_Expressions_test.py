"""
Simple syntax tests along with 1 gibberish 1 empty 1 whitespace test
"""


def test_1(calc_handler):
    result, error_list = calc_handler.run_single_exp("2*^3")
    assert result is None
    assert error_list[0].get_error_type() == "Missing_Operands_Error"


def test_2(calc_handler):
    result, error_list = calc_handler.run_single_exp("2*")
    assert result is None
    assert error_list[0].get_error_type() == "Missing_Operands_Error"


def test_3(calc_handler):
    result, error_list = calc_handler.run_single_exp("(+)")
    assert result is None
    assert error_list[0].get_error_type() == "Missing_Operands_Error"


def test_4(calc_handler):
    result, error_list = calc_handler.run_single_exp("(2+2")
    assert result is None
    assert error_list[0].get_error_type() == "Missing_Close_Paren_Error"


def test_5(calc_handler):
    result, error_list = calc_handler.run_single_exp("(-123)#")
    assert result is None
    assert error_list[0].get_error_type() == "Invalid_Hash_Error"


def test_gibberish(calc_handler):
    result, error_list = calc_handler.run_single_exp("asdasdasdasgLDLA")
    assert result is None
    assert error_list[0].get_error_type() == "Invalid_Chars_Error"


def test_empty_input(calc_handler):
    result, error_list = calc_handler.run_single_exp("")
    assert result is None
    assert error_list[0].get_error_type() == "Empty_Input_Error"


def test_whitespaces(calc_handler):
    result, error_list = calc_handler.run_single_exp("1                 +               2")
    assert error_list is None
    assert result == 3
