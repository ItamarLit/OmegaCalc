from ErrorHandler import ErrorHandler
from Errors import EvaluationError
from Tokenizer import Token
from Operators import IUnaryOperator


class Evaluator:
    """
    This class will evaluate the given postfix expression, it will catch the following errors:
    1. missing operands for binary and unary ops
    2. invalid double operands
    """

    def __init__(self, error_handler: ErrorHandler):
        self._error_handler = error_handler
        self._calculation_stack = []

    def eval(self, post_fix_token_list: list):
        for token in post_fix_token_list:
            if token.get_token_type() == "Number":
                self._handle_number_token(token)
            else:
                # op token
                self.handle_operator_token(token)

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
        token_type = token.get_token_type()
        if isinstance(token_class, IUnaryOperator):
            # unary op
            if len(self._calculation_stack) > 0:
                # eval the unary op and push it back to the stack
                self._calculation_stack.append(token_class.unary_evaluate(self._calculation_stack.pop()))
            else:
                # error missing operand for a unary token
                self._error_handler.add_error(EvaluationError(f"Missing operand for unary operator: {token_type} at position: " + str(token.get_token_pos()[0])))
        else:
            # binary op
            if len(self._calculation_stack) > 1:
                second_operand = self._calculation_stack.pop()
                first_operand = self._calculation_stack.pop()
                # eval the binary op and push it back
                self._calculation_stack.append(token_class.binary_evaluate(first_operand, second_operand))
            else:
                # error missing operand for binary op
                if len(self._calculation_stack) == 0:
                    self._error_handler.add_error(
                        EvaluationError(
                            f"Missing operands for binary operator: {token_type} at position: " + str(token.get_token_pos()[0])))
                else:
                    self._error_handler.add_error(
                        EvaluationError(
                            f"Missing operand for binary operator: {token_type} at position: " + str(token.get_token_pos()[0])))

    def _handle_number_token(self, token):
        """
        Func that adds a number to the stack as a float
        :param token:
        :return:
        """
        self._calculation_stack.append(float(token.get_token_value()))

    def clear_evaluator(self):
        self._calculation_stack = []
