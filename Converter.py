from ErrorHandler import ErrorHandler
from Tokenizer import Token
from Operators import Operator, IUnaryOperator, UMinus
from Errors import ConversionError


class Converter:
    """
    Class that converts an infix token list into a postfix token list
    The possible errors to get while converting are:
    1. Invalid paren ie missing ( to a ) token or missing ) to a (
    2. Invalid use of the ~ op ie it is not in front of a binary minus or a number
    3. Invalid unary minus use, ie it isnt before (, a number or another unary minus to the right
    The output list will be a list of tokens in postfix so that i can give better errors in the evaluator (get the position of the error)
    """

    def __init__(self, error_handler: ErrorHandler):
        self._error_handler = error_handler
        self._output_lst = []
        self._op_stack = []

    def convert(self, token_list):
        # convert infix token list to post fix
        cur_index = 0
        for token in token_list:
            if token.get_token_type() == "Number":
                self._handle_number(token)
            elif isinstance(token.get_token_value(), Operator):
                self._handle_operator(token, cur_index, token_list)
                # check if we are on a tilda and if it is valid
                if token.get_token_type() == '~' and not self._check_tilda_op(cur_index, token_list):
                    self._error_handler.add_error(
                        ConversionError("Invalid use of ~ op at pos: " + str(token.get_token_pos()[0])))
            else:
                # the token is paren
                self._handle_paren(token)
            cur_index += 1
        # call the end of input func
        self._handle_end_input()
        # check if we need to show errors
        self._error_handler.check_errors()


    def _check_tilda_op(self, cur_index, token_list):
        """
        Func that checks if the tilda is recieved in a valid way
        :param cur_index:
        :param token_list:
        :return:
        """
        # the tilda op can only come before a unary minus or a number
        if token_list[cur_index + 1].get_token_type() != "Number" and not isinstance(token_list[cur_index + 1].get_token_value(), UMinus):
            return False
        return True

    def _handle_number(self, token):
        """
        Adds a number literal to the output list
        :param token:
        :return:
        """
        self._output_lst.append(token)

    def _handle_paren(self, token):
        """
        Handles the paren
        :param token:
        :return:
        """
        if token.get_token_value() == '(':
            self._op_stack.append(token)
        else:
            # paren is )
            if self._check_list_for_paren('('):
                while len(self._op_stack) != 0 and self._op_stack[-1].get_token_value() != '(':
                    self._output_lst.append(self._op_stack.pop())
                # pop the final paren
                self._op_stack.pop()
            else:
                self._error_handler.add_error(
                    ConversionError("Missing Opening parentheses to opening parentheses at position: " + str(token.get_token_pos()[0])))

    def _check_list_for_paren(self, paren_type: chr) -> bool:
        """
        Func to check if the op_stack has an opening paren
        :return:
        """
        for token in self._op_stack:
            if token.get_token_type() == paren_type:
                return True
        return False

    def _handle_operator(self, token, cur_index, token_list):
        """
        Func that will handle operator adding to the output list
        :param token:
        :return:
        """
        current_op = token.get_token_value()
        # check if the token is unary
        if isinstance(current_op, IUnaryOperator):
            self._check_unary_minus(cur_index, token_list)
            self._op_stack.append(token)
        else:
            # binary op
            while len(self._op_stack) != 0 and self._op_stack[-1].get_token_value() != '(' and \
                    self.check_precedence(current_op, self._op_stack[-1].get_token_value()) <= 0 and len(self._output_lst) != 0:
                self._output_lst.append(self._op_stack.pop())
            self._op_stack.append(token)

    def _check_unary_minus(self, cur_index, token_list):
        """
        Func that checks that a unary minus is in a correct place
        :param cur_index:
        :return:
        """
        if token_list[cur_index].get_token_type() == "U-":
            next_token = token_list[cur_index + 1]

            if next_token.get_token_type() != "Number" and next_token.get_token_type() != ")" and next_token.get_token_type() != "U-":
                # add the error to the error handler
                self._error_handler.add_error(ConversionError(f"Invalid use of unary minus operator at position: {token_list[cur_index].get_token_pos()[0]}"
                                                              f" cannot come before: {next_token.get_token_type()}"))


    def _handle_end_input(self):
        """
        Func that will add the final ops to the output list
        :return:
        """
        if self._check_list_for_paren('('):
            # invalid exp missing ) to opening paren, get the indexes
            invalid_indexes = list(filter(lambda pos: self._op_stack[pos].get_token_value() == '(', range(len(self._op_stack))))
            for index in invalid_indexes:
                # add the error
                self._error_handler.add_error(
                    ConversionError("Missing Closing parentheses to opening parentheses at position: " + str(self._op_stack[index].get_token_pos()[0])))
        else:
            while len(self._op_stack) != 0:
                self._output_lst.append(self._op_stack.pop())

    def check_precedence(self, op_token1: Token, op_token2: Token) -> int:
        """
        This func will return:
        neg num if op1 < op2
        pos num if op1 > op2
        0 if op1 == op2
        :param op_token1:
        :param op_token2:
        :return: int value
        """
        return op_token1.get_precedence() - op_token2.get_precedence()

    def get_post_fix(self):
        """
        :return: return the postfix list
        """
        return self._output_lst

    def clear_converter(self):
        """
        Clear the used values
        :return:
        """
        self._op_stack = []
        self._output_lst = []
