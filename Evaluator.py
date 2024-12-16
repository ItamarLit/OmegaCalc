from ErrorHandler import ErrorHandler
from Errors import BaseCalcError, InvalidFactorialError, InvalidHashError
from Operators import IUnaryOperator


class Evaluator:
    """
    This class will evaluate the given postfix expression, it will catch the following errors:
    1. invalid division attempt (by 0)
    2. invalid attempt to use ! on a negative number
    Any error that occurs in this stage is a fatal one because we can't continue to evaluate if we can't preform an
    operation on a prev token, so when we encounter an error in this stage we stop the eval process
    """

    def __init__(self, error_handler: ErrorHandler):
        self._error_handler = error_handler
        self._calculation_stack = []
        self._encountered_fatal_error = False

    def eval(self, post_fix_token_list: list):
        """
        Main eval func that takes the post fix list and converts it into a single number if possible
        :param post_fix_token_list:
        """
        for token in post_fix_token_list:
            if not self._encountered_fatal_error:
                if token.get_token_type() == "Number":
                    self._handle_number_token(token)
                else:
                    # op token
                    self.handle_operator_token(token)
        # check if we need to show errors
        self._error_handler.check_errors()

    def get_final(self):
        # get the final evaled num
        # check if the value has decimal point
        final_value = self._calculation_stack.pop()
        if final_value % 1 == 0:
            final_value = int(final_value)
        return final_value

    def handle_operator_token(self, token):
        """
        Func that handles the operator evaluation, checks if the operator is unary or binary then attempts
        to preform its func
        :param token:
        """
        token_class = token.get_token_value()
        if isinstance(token_class, IUnaryOperator):
            # unary op
            num_val = self._calculation_stack.pop()
            try:
                self._calculation_stack.append(token_class.unary_evaluate(num_val))
            except InvalidFactorialError as e:
                self._error_handler.add_error(BaseCalcError("Invalid_Factorial_Error", e))
                self._encountered_fatal_error = True
            except OverflowError as e:
                self._error_handler.add_error(BaseCalcError("Factorial_Overflow_Error", e))
                self._encountered_fatal_error = True
            except InvalidHashError:
                self._error_handler.add_error(BaseCalcError("Invalid_Hash_Error",
                    f"Cannot perform hash at position: {token.get_token_pos()[0]} invalid negative num: {num_val}"))
                self._encountered_fatal_error = True
            except Exception as e:
                # this should never happen but is used as a safeguard
                self._error_handler.add_error(BaseCalcError("Safe_Guard_Error", e))
        else:
            second_operand = self._calculation_stack.pop()
            first_operand = self._calculation_stack.pop()
            # eval the binary op and push it back
            try:
                self._calculation_stack.append(token_class.binary_evaluate(first_operand, second_operand))
            except ZeroDivisionError:
                self._error_handler.add_error(BaseCalcError("Zero_Div_Error", f"Cannot divide value by 0"))
                self._encountered_fatal_error = True
            except ValueError as e:
                self._error_handler.add_error(BaseCalcError("Zero_Pow_Error", e))
                self._encountered_fatal_error = True
            except OverflowError as e:
                self._error_handler.add_error(BaseCalcError("Pow_Overflow_Error", "Power operation result is too large."))
                self._encountered_fatal_error = True
            except Exception as e:
                # this should never happen but is used as a safeguard
                self._error_handler.add_error(BaseCalcError("Safe_Guard_Error", e))

    def _handle_number_token(self, token):
        """
        Func that adds a number to the stack as a float
        :param token:
        """
        self._calculation_stack.append(float(token.get_token_value()))

    def clear_evaluator(self):
        """
        Func that clears the evaluator of used data, so that it can be used for the next expression
        """
        self._calculation_stack = []
        self._encountered_fatal_error = False

