from ErrorHandler import ErrorHandler
from Operators import Operator, UMinus
from Errors import BaseCalcError
from Tokenizer import Token


class Converter:
    """
    Class that converts an infix token list into a postfix token list
    The possible errors to get while converting are:
    1. Invalid parentheses, missing ( to a ) token or missing ) to a (
    2. Invalid operator usage (double operators / invalid unary op usage)
    3. Invalid parentheses use check that there is a binary op before and after parentheses if they have a number next to them
    4. empty parenthesis
    The output list will be a list of tokens in postfix so that I can give better errors in the evaluator (get the position of the error)
    """

    def __init__(self, error_handler: ErrorHandler):
        self._error_handler = error_handler
        self._output_lst = []
        self._op_stack = []
        self._hit_missing_operands_error = False
        self._signed_minus_indexes = []
        self._unary_sign_token = Token("U-", UMinus(8, '-', "left", ""), -1, -1)

    def convert(self, token_list: list):
        """
        This is the main convert function, it goes over the token list and turns it into a post fix token list
        :param token_list:
        """
        # convert infix token list to post fix
        cur_index = 0
        for token in token_list:
            if token.get_token_type() == "Number":
                self._handle_number(token)
            elif isinstance(token.get_token_value(), Operator):
                self._check_operator_placement(cur_index, token_list)
                self._handle_operator(token, cur_index, token_list)
            else:
                # the token is parentheses
                self._handle_paren(token_list, cur_index)
            cur_index += 1
        # call the end of input func
        self._handle_end_input()
        # check if we need to show errors
        self._error_handler.check_errors()

    def _handle_number(self, token: Token):
        """
        Adds a number literal to the output list
        :param token:
        """
        self._output_lst.append(token)

    def _handle_paren(self, token_list: list, cur_index: int):
        """
        Handles the parentheses
        :param token_list:
        :param cur_index:
        """
        # add invalid parentheses errors if there are any
        self._check_invalid_paren(token_list, cur_index)
        cur_token = token_list[cur_index]
        if cur_token.get_token_value() == '(':
            # check for binary op
            self._op_stack.append(cur_token)
        else:
            # parentheses is )
            if self._check_list_for_paren('('):
                while len(self._op_stack) != 0 and self._op_stack[-1].get_token_value() != '(':
                    self._output_lst.append(self._op_stack.pop())
                # pop the final parentheses
                self._op_stack.pop()
            else:
                self._error_handler.add_error(
                    BaseCalcError("Missing Opening parentheses to closing parentheses at position: " + str(
                        cur_token.get_token_pos()[0])))

    def _check_invalid_paren(self, token_list: list, cur_index: int):
        """
        Checks for any errors with parentheses in the expression.
        """
        cur_token = token_list[cur_index]
        cur_paren = cur_token.get_token_type()
        pos = cur_token.get_token_pos()[0]
        prev_token = token_list[cur_index - 1] if cur_index - 1 >= 0 else None
        next_token = token_list[cur_index + 1] if cur_index + 1 < len(token_list) else None
        if cur_paren == '(':
            self._check_opening_paren(prev_token, next_token, pos)
        else:
            self._check_closing_paren(prev_token, next_token, pos)

    def _check_opening_paren(self, prev_token: Token, next_token: Token, pos: int):
        """
        Check all errors with opening parentheses
        :param prev_token:
        :param next_token:
        :param pos:
        """
        # check token before (
        if prev_token and prev_token.get_token_type() in ['!', 'Number']:
            self._error_handler.add_error(
                BaseCalcError(f"Invalid token before ( at position: {pos}")
            )

        next_type = next_token.get_token_type()
        # check for empty parentheses
        if next_type == ')':
            closing_pos = next_token.get_token_pos()[0]
            self._error_handler.add_error(
                BaseCalcError(f"Invalid empty parentheses at position: {closing_pos - 1} -> {closing_pos}")
            )

    def _check_closing_paren(self, prev_token: Token, next_token: Token, pos: int):
        """
        Check all errors with closing parentheses
        :param prev_token:
        :param next_token:
        :param pos:
        """
        if not prev_token:
            self._error_handler.add_error(
                BaseCalcError(f"Invalid ) at position: {pos} (no opening parenthesis)")
            )
            return
        # check token after )
        if next_token and next_token.get_token_type() in ["U-", "Number"]:
            self._error_handler.add_error(
                BaseCalcError(f"Invalid token after ) at position: {pos}")
            )

    def _check_list_for_paren(self, paren_type: chr) -> bool:
        """
        Func to check if the op_stack has an opening parentheses
        :return:
        """
        for token in self._op_stack:
            if token.get_token_type() == paren_type:
                return True
        return False

    def _handle_operator(self, token: Token, cur_index: int, token_list: list):
        """
        Func that will handle operator adding to the output list
        :param token:
        """
        current_op = token.get_token_value()
        if self._check_for_sign_minus(cur_index, token_list):
            # append sign minuses immediately
            self._op_stack.append(self._unary_sign_token)
        else:
            while len(self._op_stack) != 0 and self._op_stack[-1].get_token_value() != '(' and \
                    self.check_precedence(current_op, self._op_stack[-1].get_token_value()) <= 0 and len(self._output_lst) != 0:
                self._output_lst.append(self._op_stack.pop())
            self._op_stack.append(token)

    def _handle_end_input(self):
        """
        Func that will add the final ops to the output list
        """
        if self._check_list_for_paren('('):
            # invalid exp missing ) to opening parentheses, get the indexes
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

    def get_post_fix(self) -> list:
        """
        :return: return the postfix list
        """
        return self._output_lst

    def clear_converter(self):
        """
        Clear the used values so i can convert another expression
        """
        self._op_stack = []
        self._output_lst = []
        self._signed_minus_indexes = []

    def _check_operator_placement(self, cur_index: int, token_list: list):
        """
        This func will check if an operator is placed in a valid way based on its placemnte
        :param cur_index:
        :param token_list:
        """
        if self._hit_missing_operands_error:
            self._hit_missing_operands_error = False
            return
        current_token = token_list[cur_index]
        current_token_placment = current_token.get_token_value().get_placement()
        check_funcs_dict = {
            "left": self._check_left_op,
            "right": self._check_right_op,
            "mid": self._check_mid_op,
        }
        func = check_funcs_dict[current_token_placment]
        if not func(cur_index, token_list):
            if current_token_placment != "mid":
                self._error_handler.add_error(
                    BaseCalcError(
                        f"Invalid use of {current_token.get_token_value().get_op_value()} at position: {current_token.get_token_pos()[0]}"))
            else:
                self._error_handler.add_error(
                    BaseCalcError(
                        f"Missing operands for: {current_token.get_token_type()} at position: {current_token.get_token_pos()[0]}"))
                if cur_index + 1 < len(token_list) and isinstance(token_list[cur_index + 1].get_token_value(), Operator):
                    self._hit_missing_operands_error = True

    def _check_left_op(self, cur_index: int, token_list: list) -> bool:
        """
        Func to check the validity of a left sided operator
        :param cur_index:
        :param token_list:
        :return: False if non valid, else true
        """
        cur_type = token_list[cur_index].get_token_type()
        next_token = token_list[cur_index + 1] if cur_index + 1 < len(token_list) else None
        if next_token is None:
            return False
        next_type = next_token.get_token_type()
        if cur_type == '~':
            # for tilda we check that it isnt between two numbers as this is illegal we can do that
            # by checking if it is a valid right op and then we know it is invalid tilda usage
            return next_type in ("U-", "Number") and not self._check_right_op(cur_index, token_list)
        elif cur_type == "U-":
            return next_type in ("Number", "(", "U-")
        else:
            return next_type in ("Number", "(", "U-", "~")

    def _check_right_op(self, cur_index: int, token_list: list) -> bool:
        """
        Func to check the validity of a right sided operator
        :param cur_index:
        :param token_list:
        :return: False if non valid, else true
        """
        prev_token = token_list[cur_index - 1] if cur_index - 1 >= 0 else None
        if prev_token is None:
            return False
        prev_type = prev_token.get_token_type()
        return prev_type in ("Number", ")", "!", '#')

    def _check_mid_op(self, cur_index: int, token_list: list) -> bool:
        """
        Func that checks the validity of an operator that is binary
        :param cur_index:
        :param token_list:
        :return: False if non valid, else true
        """
        return self._check_right_op(cur_index, token_list) and self._check_left_op(cur_index, token_list)

    def _check_for_sign_minus(self, cur_index: int, token_list: list) -> bool:
        """
        Func to check if a unary minus is a sign minus
        A sign minus is the highest precedence op and must be pushed before anything else
        :param cur_index:
        :param token_list:
        :return: True if it is a sign minus, False if it isnt
        """
        cur_type = token_list[cur_index].get_token_type()
        cur_value = token_list[cur_index].get_token_value()
        if cur_type != "U-":
            return False
        # if the prev minus was a signed one the current one is as well
        if cur_index != 0 and (cur_index - 1) in self._signed_minus_indexes:
            self._signed_minus_indexes.append(cur_index)
            return True
        # token is U-
        prev_token = token_list[cur_index - 1] if cur_index - 1 >= 0 else None
        if prev_token is None or prev_token.get_token_type() == "(":
            return False
        self._signed_minus_indexes.append(cur_index)
        return True
