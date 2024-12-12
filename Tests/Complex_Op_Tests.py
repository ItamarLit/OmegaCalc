"""
Complex operations tests
"""

def test_1(calc_handler):
    result, error_list = calc_handler.run_single_exp("((1+1*3^-2)$8*9!+~--3)%3@2")
    assert result == 2
    assert error_list is None

def test_2(calc_handler):
    result, error_list = calc_handler.run_single_exp("(91#*21^3---2!+15)@1/19")
    assert result == 2437.473684
    assert error_list is None

def test_3(calc_handler):
    result, error_list = calc_handler.run_single_exp("((3$-2+15!#)#--(-43)%34)+(0.1-0.56)")
    assert result == 2.54
    assert error_list is None

def test_4(calc_handler):
    result, error_list = calc_handler.run_single_exp("((3$-2+15!#)#--(-43)%34)+(0.1-0.56)")
    assert result == 2.54
    assert error_list is None

def test_5(calc_handler):
    result, error_list = calc_handler.run_single_exp("((3$-2+15!#)#--(-43)%34)+(0.1-0.56)")
    assert result == 2.54
    assert error_list is None