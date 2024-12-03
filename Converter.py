from ErrorHandler import ErrorHandler
from Tokenizer import Token
from Operators import Operator

class Converter:
    """
    Class that converts an infix token list into a postfix token list
    The possible errors to get while converting are:
    1.
    2.
    """

    def __init__(self, error_handler: ErrorHandler):
        self._error_handler = error_handler
        self._output_lst = []
        self._op_stack = []
        # dict to hold the handlers
        self.handlers = {
            0: self.__handle_number,
            1: self.__handle_paren,
            2: self.__handle_operator,
        }

    def convert(self, token_list):
        # convert infix token list to post fix
        for token in token_list:
            # go over the handler dict and get the correct handler
            handle_func = self.handlers[self.__get_handler_key(token)]
            # call the handle func
            handle_func(token)
        # call the end of input func
        self.__handle_end_input()

    def __get_handler_key(self, token):
        """
        This func maps the token type to the handler dict key
        :param token:
        :return:
        """
        if token.get_token_type() == "Number":
            return 0
        elif isinstance(token.get_token_value(), Operator):
            return 2
        return 1

    def __handle_number(self, token):
        """
        Adds a number literal to the output list
        :param token:
        :return:
        """
        self._output_lst.append(float(token.get_token_value()))

    def __handle_paren(self, token):
        """
        Handles the paren
        :param token:
        :return:
        """
        if token.get_token_value() == '(':
            self._op_stack.append(token.get_token_value())
        else:
            # paren is )
            while len(self._op_stack) != 0 and self._op_stack[-1] != '(':
                self._output_lst.append(self._op_stack.pop().get_op_value())
            # pop the final paren
            self._op_stack.pop()

    def __handle_operator(self, token):
        while len(self._op_stack) != 0 and self._op_stack[-1] != '(' and \
                self.check_precedence(token.get_token_value(), self._op_stack[-1]) <= 0 and len(self._output_lst) != 0:
            self._output_lst.append(self._op_stack.pop().get_op_value())
        self._op_stack.append(token.get_token_value())

    def __handle_end_input(self):
        while len(self._op_stack) != 0:
            self._output_lst.append(self._op_stack.pop().get_op_value())

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

    def get_rpn(self):
        return self._output_lst

    def clear_converter(self):
        self._op_stack = []
        self._output_lst = []