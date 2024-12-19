"""
Error tests for all the errors in the calc
"""


def test_factorial_negative(calc_handler):
    result, error_list = calc_handler.run_single_exp("(-3)!")
    assert result == None
    assert error_list[0].get_error_type() == "Invalid_Factorial_Error"


def test_factorial_float(calc_handler):
    result, error_list = calc_handler.run_single_exp("0.3!")
    assert result == None
    assert error_list[0].get_error_type() == "Invalid_Factorial_Error"


def test_hash_negative(calc_handler):
    result, error_list = calc_handler.run_single_exp("~123#")
    assert result == None
    assert error_list[0].get_error_type() == "Invalid_Hash_Error"


def test_zero_div(calc_handler):
    result, error_list = calc_handler.run_single_exp("1/0")
    assert result == None
    assert error_list[0].get_error_type() == "Zero_Div_Error"


def test_overflow_power(calc_handler):
    result, error_list = calc_handler.run_single_exp("1000000000000^1000000000000")
    assert result == None
    assert error_list[0].get_error_type() == "Pow_Overflow_Error"


def test_overflow_factorial(calc_handler):
    result, error_list = calc_handler.run_single_exp("100000000000!")
    assert result == None
    assert error_list[0].get_error_type() == "Large_Number_Error"


def test_overflow_hashtag(calc_handler):
    result, error_list = calc_handler.run_single_exp("999999999999999999999999999999999999999999999.1#")
    assert result == None
    assert error_list[0].get_error_type() == "Large_Number_Error"


def test_invalid_power_attempt(calc_handler):
    result, error_list = calc_handler.run_single_exp("0^-1")
    assert result == None
    assert error_list[0].get_error_type() == "Zero_Pow_Error"


def test_number_error(calc_handler):
    result, error_list = calc_handler.run_single_exp("12..14+123.+.3")
    assert result == None
    for error in error_list:
        assert error.get_error_type() == "Number_Error"


def test_invalid_char(calc_handler):
    result, error_list = calc_handler.run_single_exp("a+c+123")
    assert result == None
    for error in error_list:
        assert error.get_error_type() == "Invalid_Char_Error"


def test_invalid_chars(calc_handler):
    result, error_list = calc_handler.run_single_exp("abc+bcd+123")
    assert result == None
    for error in error_list:
        assert error.get_error_type() == "Invalid_Chars_Error"


def test_empty_input(calc_handler):
    result, error_list = calc_handler.run_single_exp("")
    assert result == None
    assert error_list[0].get_error_type() == "Empty_Input_Error"


def test_missing_open_paren(calc_handler):
    result, error_list = calc_handler.run_single_exp("1+2)")
    assert result == None
    assert error_list[0].get_error_type() == "Missing_Open_Paren_Error"


def test_invalid_before_open_paren(calc_handler):
    result, error_list = calc_handler.run_single_exp("1(1-2)")
    assert result == None
    assert error_list[0].get_error_type() == "Invalid_Before_Open_Paren_Error"


def test_invalid_empty_paren_error(calc_handler):
    result, error_list = calc_handler.run_single_exp("1+()+2")
    assert result == None
    assert error_list[0].get_error_type() == "Invalid_Empty_Paren_Error"


def test_missing_close_paren_error(calc_handler):
    result, error_list = calc_handler.run_single_exp("(1+2")
    assert result == None
    assert error_list[0].get_error_type() == "Missing_Close_Paren_Error"


def test_missing_operands_error(calc_handler):
    result, error_list = calc_handler.run_single_exp("1++2+2**3")
    assert result == None
    for error in error_list:
        assert error.get_error_type() == "Missing_Operands_Error"


def test_invalid_unary_usage(calc_handler):
    result, error_list = calc_handler.run_single_exp("-~3")
    assert result == None
    assert error_list[0].get_error_type() == "Invalid_Unary_Usage_Error"


def test_missing_operand_error(calc_handler):
    result, error_list = calc_handler.run_single_exp("#~")
    assert result == None
    for error in error_list:
        assert error.get_error_type() == "Missing_Operand_Error"
