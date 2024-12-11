from ErrorHandler import ErrorHandler
from Operators import Operator, IUnaryOperator, IBinaryOperator, UMinus
from Errors import BaseCalcError


class Converter:
    """
    Class that converts an infix token list into a postfix token list
    The possible errors to get while converting are:
    1. Invalid paren ie missing ( to a ) token or missing ) to a (
    2. Invalid use of the ~ op ie it is not in front of a binary minus or a number
    3. Invalid use of the ! op ie no number or ) infront of it
    4. Invalid unary minus use, ie it isn't before (, a number or another unary minus to the right
    5. Invalid paren use check that there is a binary op before and after paren if they have a number next to them
    6. empty parenthesis
    The output list will be a list of tokens in postfix so that I can give better errors in the evaluator (get the position of the error)
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
                        BaseCalcError("Invalid use of ~ op at pos: " + str(token.get_token_pos()[0])))
            else:
                # the token is paren
                self._handle_paren(token_list, cur_index)
            cur_index += 1
        # call the end of input func
        self._handle_end_input()
        # check if we need to show errors
        self._error_handler.check_errors()

    def _check_tilda_op(self, cur_index, token_list):
        """
        Func that checks if the tilda is received in a valid way
        :param cur_index:
        :param token_list:
        :return:
        """
        next_token = token_list[cur_index + 1] if cur_index + 1 < len(token_list) else None
        prev_token = token_list[cur_index - 1] if cur_index - 1 >= 0 else None
        # the tilda op can only come before a unary minus or a number and before the tilda there was nothing or a binary op
        if next_token.get_token_type() != "Number" and not isinstance(next_token.get_token_value(), UMinus):
            return False
        if prev_token is not None and not isinstance(prev_token.get_token_value(), IBinaryOperator) and\
                prev_token.get_token_type() != '(':
            return False
        return True

    def _handle_number(self, token):
        """
        Adds a number literal to the output list
        :param token:
        :return:
        """
        self._output_lst.append(token)

    def _handle_paren(self, token_list, cur_index):
        """
        Handles the paren
        :param token_list:
        :param cur_index:
        :return:
        """
        # add invalid paren errors if there are any
        self._check_invalid_paren(token_list, cur_index)

        cur_token = token_list[cur_index]
        if cur_token.get_token_value() == '(':
            # check for binary op
            self._op_stack.append(cur_token)
        else:
            # paren is )
            if self._check_list_for_paren('('):
                while len(self._op_stack) != 0 and self._op_stack[-1].get_token_value() != '(':
                    self._output_lst.append(self._op_stack.pop())
                # pop the final paren
                self._op_stack.pop()
            else:
                self._error_handler.add_error(
                    BaseCalcError("Missing Opening parentheses to closing parentheses at position: " + str(
                        cur_token.get_token_pos()[0])))

    def _check_invalid_paren(self, token_list, cur_index):
        """
        This func is used to check for any errors in the expression that have to do with paren
        :param token_list:
        :param cur_index:
        :return:
        """
        cur_paren = token_list[cur_index].get_token_type()
        next_token = token_list[cur_index + 1] if cur_index + 1 < len(token_list) else None
        prev_token = token_list[cur_index - 1] if cur_index - 1 >= 0 else None

        # opening paren, check if next token is a binary op or !
        if cur_paren == '(':
            # ( can never finish an exp so i dont need to check if cur_index + 1 is none
            next_token_type = next_token.get_token_type()
            next_token_value = next_token.get_token_value()

            # check that the token before the paren is not a number or !
            if prev_token is not None and (
                    prev_token.get_token_type() == '!' or prev_token.get_token_type() == "Number"):
                self._error_handler.add_error(BaseCalcError(
                    f"Invalid token before opening parentheses at position: {token_list[cur_index].get_token_pos()[0]}"))

            if isinstance(next_token_value, IBinaryOperator) or next_token_type == '!':
                self._error_handler.add_error(BaseCalcError(
                      f"Missing operands for token: {next_token_type} at position:"
                    f" {token_list[cur_index + 1].get_token_pos()[0]}"))
                return

            elif next_token_type == ')':
                closing_paren_index = token_list[cur_index + 1].get_token_pos()[0]
                self._error_handler.add_error(BaseCalcError(
                    f"Invalid empty parentheses at position: {closing_paren_index - 1} -> {closing_paren_index}"))
                return

        # closing paren
        else:
            prev_token_type = token_list[cur_index - 1].get_token_type()
            prev_token_value = token_list[cur_index - 1].get_token_value()
            if isinstance(prev_token_value, IBinaryOperator) or (
                    prev_token_type != '!' and isinstance(prev_token_value, IUnaryOperator)):
                self._error_handler.add_error(BaseCalcError(
                    f"Missing operands for token: {prev_token_type} at position:"
                    f" {token_list[cur_index - 1].get_token_pos()[0]}"))
            # check that the token before the paren is not a number or !
            if next_token is not None and (next_token.get_token_type() == "U-"
                                             or next_token.get_token_type() == "Number"):
                self._error_handler.add_error(BaseCalcError(
                    f"Invalid token after closing parentheses at position: {token_list[cur_index].get_token_pos()[0]}"))


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
        while len(self._op_stack) != 0 and self._op_stack[-1].get_token_value() != '(' and \
                self.check_precedence(current_op, self._op_stack[-1].get_token_value()) <= 0 and len(
            self._output_lst) != 0:
            self._output_lst.append(self._op_stack.pop())
        self._op_stack.append(token)


    def _check_unary_minus(self, cur_index, token_list):
        """
        Func that checks that a unary minus is in a correct place
        :param cur_index:
        :return:
        """
        if token_list[cur_index].get_token_type() == "U-":
            if len(token_list) > 1:
                next_token = token_list[cur_index + 1]

                if next_token.get_token_type() != "Number" and next_token.get_token_type() != "(" and next_token.get_token_type() != "U-":
                    # add the error to the error handler
                    self._error_handler.add_error(BaseCalcError(
                        f"Invalid use of unary minus operator at position: {token_list[cur_index].get_token_pos()[0]}"
                        f" cannot come before: {next_token.get_token_type()}"))
            else:
                self._error_handler.add_error(BaseCalcError(
                    f"Invalid use of unary minus operator at position: {token_list[cur_index].get_token_pos()[0]}"))

    def _handle_end_input(self):
        """
        Func that will add the final ops to the output list
        :return:
        """
        if self._check_list_for_paren('('):
            # invalid exp missing ) to opening paren, get the indexes
            invalid_indexes = list(
                filter(lambda pos: self._op_stack[pos].get_token_value() == '(', range(len(self._op_stack))))
            for index in invalid_indexes:
                # add the error
                self._error_handler.add_error(
                    BaseCalcError("Missing Closing parentheses to opening parentheses at position: " + str(
                        self._op_stack[index].get_token_pos()[0])))
        else:
            while len(self._op_stack) != 0:
                self._output_lst.append(self._op_stack.pop())

    def check_precedence(self, op_token1: Operator, op_token2: Operator) -> int:
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

    def _check_factorial(self, cur_index, token_list):
        if token_list[cur_index].get_token_type() == '!':
            prev_token = token_list[cur_index - 1]
            if prev_token.get_token_type() != ")" and prev_token.get_token_type() != "Number":
                self._error_handler.add_error(BaseCalcError(f"Invalid use of ! operator at position: {token_list[cur_index].get_token_pos()[0]}"))