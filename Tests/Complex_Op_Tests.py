"""
Complex operations tests
"""


def test_1(calc_handler):
    result, error_list = calc_handler.run_single_exp("((1+1*3^-2)$8*9!+~--3)%3@2")
    assert result == 2
    assert error_list is None


def test_2(calc_handler):
    result, error_list = calc_handler.run_single_exp("(91#*21^3---2!+15)@1/19")
    assert result == 2437.4736842105262
    assert error_list is None


def test_3(calc_handler):
    result, error_list = calc_handler.run_single_exp("((3$-2+15!#)#--(-43)%34)+(0.1-0.56)")
    assert result == 2.54
    assert error_list is None


def test_4(calc_handler):
    result, error_list = calc_handler.run_single_exp("((12#-3!)$23)^(2*13+~26)%3")
    assert result == 1
    assert error_list is None


def test_5(calc_handler):
    result, error_list = calc_handler.run_single_exp("((~-32*2^-5)#-16%2)+(16@12)--12")
    assert result == 27
    assert error_list is None


def test_6(calc_handler):
    result, error_list = calc_handler.run_single_exp("(((9*9)#!--12*15+3-2)#^2.5)&0.512")
    assert result == 0.512
    assert error_list is None


def test_7(calc_handler):
    result, error_list = calc_handler.run_single_exp("(~-23##!-(12*2@3^5)&12+33)#")
    assert result == 6
    assert error_list is None


def test_8(calc_handler):
    result, error_list = calc_handler.run_single_exp("(((3^4.5-12.2)@3.21)##!)#^0.2*100")
    assert result == 193.3182044931763
    assert error_list is None


def test_9(calc_handler):
    result, error_list = calc_handler.run_single_exp("((-(21%6)#+12)@12)-~13*12^6$8")
    assert result == 5589762058.5
    assert error_list is None


def test_10(calc_handler):
    result, error_list = calc_handler.run_single_exp("((5!+6^3)@((7%2)$9))#-~3^2")
    assert result == 6
    assert error_list is None


def test_11(calc_handler):
    result, error_list = calc_handler.run_single_exp("(((12&7)*((3^4)-5!))*-1)#^2*-1")
    assert result == -144
    assert error_list is None


def test_12(calc_handler):
    result, error_list = calc_handler.run_single_exp("((-(15*3)%8)+7)-~4^2$5")
    assert result == 1026
    assert error_list is None


def test_13(calc_handler):
    result, error_list = calc_handler.run_single_exp("(12+(-8%3)^4@6)-~5*9$7")
    assert result == 25
    assert error_list is None


def test_14(calc_handler):
    result, error_list = calc_handler.run_single_exp("((8$3)&(10%3)^(2*4))@5^2.5")
    assert result == 15.588457268119896
    assert error_list is None


def test_15(calc_handler):
    result, error_list = calc_handler.run_single_exp("(((~5)*9)@((2.0^3)+(4!))@6.5)#")
    assert result == 0
    assert error_list is None


def test_16(calc_handler):
    result, error_list = calc_handler.run_single_exp("(((10/2)^(~3$7))%5!*3#)^2")
    assert result == 225
    assert error_list is None


def test_17(calc_handler):
    result, error_list = calc_handler.run_single_exp("(((9!@3)-(10&2))/(~4)*-2)#")
    assert result == 38
    assert error_list is None


def test_18(calc_handler):
    result, error_list = calc_handler.run_single_exp("((((~10)*5!)+(7^2))@((20%7)$3))")
    assert result == -572.5
    assert error_list is None


def test_19(calc_handler):
    result, error_list = calc_handler.run_single_exp("~10*5!+7^2@(20%7$3!)-4")
    assert result == 1197
    assert error_list is None


def test_20(calc_handler):
    result, error_list = calc_handler.run_single_exp("8#-3*2+9!/(10&3^2)-~5%4")
    assert result == 40319
    assert error_list is None
