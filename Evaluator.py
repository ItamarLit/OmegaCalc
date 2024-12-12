from ErrorHandler import ErrorHandler
from Errors import BaseCalcError, InvalidFactorialError
from Operators import IUnaryOperator


class Evaluator:
    """
    This class will evaluate the given postfix expression, it will catch the following errors:
    1. missing operands for binary and unary ops
    2. invalid division attempt (by 0)
    3. invalid attempt to use ! on a negative number
    """

    def __init__(self, error_handler: ErrorHandler):
        self._error_handler = error_handler
        self._calculation_stack = []
        self._encountered_fatal_error = False

    def eval(self, post_fix_token_list: list):
        for token in post_fix_token_list:
            if token.get_token_type() == "Number":
                self._handle_number_token(token)
            else:
                # op token
                self.handle_operator_token(token)
        # check if we need to show errors
        self._error_handler.check_errors()

    def get_final(self):
        # get the final evaled num
        return self._calculation_stack.pop()

    def handle_operator_token(self, token):
        """
        Func that handles the operator evaluation
        :param token:
        :return:
        """
        token_class = token.get_token_value()
        if isinstance(token_class, IUnaryOperator):
            # unary op
            num_val = self._calculation_stack.pop()
            try:
                self._calculation_stack.append(token_class.unary_evaluate(num_val))
            except InvalidFactorialError:
                self._error_handler.add_error(BaseCalcError(
                    f"Cannot perform factorial at position: {token.get_token_pos()[0]} invalid factorial num: {num_val}"))
                self._encountered_fatal_error = True
        else:
            second_operand = self._calculation_stack.pop()
            first_operand = self._calculation_stack.pop()
            # eval the binary op and push it back
            try:
                self._calculation_stack.append(token_class.binary_evaluate(first_operand, second_operand))
            except ZeroDivisionError:
                self._error_handler.add_error(BaseCalcError(f"Cannot divide value by 0"))
                self._encountered_fatal_error = True
            except Exception as e:
                self._error_handler.add_error(BaseCalcError(e))

    def _handle_number_token(self, token):
        """
        Func that adds a number to the stack as a float
        :param token:
        :return:
        """
        self._calculation_stack.append(float(token.get_token_value()))

    def clear_evaluator(self):
        self._calculation_stack = []
        self._encountered_fatal_error = False

