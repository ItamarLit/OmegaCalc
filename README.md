This is a special calculator, here are the operators in the calculator:
'+' : Precedence 1, placement middle, This operator adds two operands
'-' : Precedence 1, placement middle, This operator subtracts two operands
'*' : Precedence 2, placement middle, This operator multiplies two operands
'/' : Precedence 2, placement middle, This operator divides two operands
'U-' : Precedence 2.5, placement left, This is the unary minus operator; it turns the sign of a given value to the negative of the current sign
'^' : Precedence 3, placement middle, This operator is the power operator
'%' : Precedence 4, placement middle, This operator is the modulo operator
'&' : Precedence 5, placement middle, This operator gives the minimum between two operands
'$' : Precedence 5, placement middle, This operator gives the maximum between two operands
'@' : Precedence 5, placement middle, This operator gives the average between two operands
'!' : Precedence 6, placement right, This operator returns the factorial of a single non-negative operand
'~' : Precedence 6, placement left, This is the negative operator
'#' : Precedence 6, placement left, This is the negative operator
This project has built-in testing ready for the user, it tests the error handling the basic syntax and complex expressions. To run the tests go to the pycharm treminal and run: pytest .\Tests\"Test_File_Name"
The calculator is built in a way that will prevent it from ever crashing, it also handles multipule error handling and use of floating point numbers.
