from ErrorHandler import ErrorHandler
from Errors import *
from Operators import IUnaryOperator


class Evaluator:
    """
    This class will evaluate the given postfix expression, it will catch the following errors:
    1. Invalid division attempt (by 0)
    2. Invalid attempt to use ! on a negative number
    3. Invalid attempt to use ! on a floating point number
    4. ! overflow
    5. Invalid attempt to do 0^(neg number)
    6. Pow overflow
    7. Invalid attempt to preform hash on a negative number
    8. Invalid attempt to preform hash on a very small / very large number
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
                    self._handle_operator_token(token)
        # check if we need to show errors
        self._error_handler.check_errors()

    def get_final(self):
        # get the final num
        # check if the value has decimal point
        final_value = self._calculation_stack.pop()
        if final_value % 1 == 0:
            final_value = int(final_value)
        return final_value

    def _set_error(self, error_type, error_msg):
        """
        Func that adds an error and sets the fatal error flag
        :param error_type:
        :param error_msg:
        """
        self._error_handler.add_error(BaseCalcError(error_type, error_msg))
        self._encountered_fatal_error = True

    def _handle_operator_token(self, token):
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
                self._set_error("Invalid_Factorial_Error", e)
            except LargeNumberError as e:
                self._set_error("Large_Number_Error", e)
            except InvalidHashError as e:
                self._set_error("Invalid_Hash_Error", e)
            except SmallNumberError as e:
                self._set_error("Small_Number_Error", e)
            except Exception as e:
                # this should never happen but is used as a safeguard
                self._set_error("Safe_Guard_Error", e)

        else:
            second_operand = self._calculation_stack.pop()
            first_operand = self._calculation_stack.pop()
            # eval the binary op and push it back
            try:
                self._calculation_stack.append(token_class.binary_evaluate(first_operand, second_operand))
            except ZeroDivisionError:
                self._set_error("Zero_Div_Error", "Cannot divide value by 0")
            except InvalidPowerError as e:
                self._set_error("Zero_Pow_Error", e)
            except PowerOverflowError as e:
                self._set_error("Pow_Overflow_Error", e)
            except Exception as e:
                # this should never happen but is used as a safeguard
                self._set_error("Safe_Guard_Error", e)

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
