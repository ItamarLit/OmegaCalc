from ErrorParts.ErrorHandler import ErrorHandler
from CalcParts.Operators import Operator, UMinus, ILeftSidedOp, IRightSidedOp
from ErrorParts.Errors import BaseCalcError
from CalcParts.Tokenizer import Token


class Converter:
    """
    Class that converts an infix token list into a postfix token list
    The possible errors to get while converting are:
    1. Invalid parentheses, missing ( to a ) token or missing ) to a (
    2. Invalid operator usage (double operators / invalid unary op usage)
    3. Invalid parentheses use check that there is a binary op before and
     after parentheses if they have a number next to them
    4. Empty parenthesis
    5. Missing operands / operand for binary and unary ops
    6. Invalid usage of unary ops (according to the rules)
    The output list will be a list of tokens in postfix so that
    I can give better errors in the evaluator (get the position of the error)
    """

    def __init__(self, error_handler: ErrorHandler):
        self._error_handler = error_handler
        self._output_lst = []
        self._op_stack = []
        self._hit_missing_operands_error = False
        self._signed_minus_indexes = []
        # sign minus with the highest priority
        self._unary_sign_token = Token("U-", UMinus(7, '-', "left", ""), -1, -1)

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
                    BaseCalcError("Missing_Open_Paren_Error",
                                  "Missing Opening parentheses to closing parentheses at position: " + str(
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
            self._check_closing_paren(next_token, pos)

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
                BaseCalcError("Invalid_Before_Open_Paren_Error", f"Invalid token before ( at position: {pos}")
            )

        next_type = next_token.get_token_type()
        # check for empty parentheses
        if next_type == ')':
            closing_pos = next_token.get_token_pos()[0]
            self._error_handler.add_error(
                BaseCalcError("Invalid_Empty_Paren_Error",
                              f"Invalid empty parentheses at position: {closing_pos - 1} -> {closing_pos}")
            )

    def _check_closing_paren(self, next_token: Token, pos: int):
        """
        Check all errors with closing parentheses
        :param next_token:
        :param pos:
        """
        if next_token and next_token.get_token_type() in ["U-", "Number"]:
            self._error_handler.add_error(
                BaseCalcError("Invalid_After_Close_Paren_Error", f"Invalid token after ) at position: {pos}")
            )

    def _check_list_for_paren(self, paren_type: chr) -> bool:
        """
        Func to check if the op_stack has parentheses of paren_type
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
                    self._check_precedence(current_op, self._op_stack[-1].get_token_value()) <= 0 and \
                    len(self._output_lst) != 0:
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
                    BaseCalcError("Missing_Close_Paren_Error",
                                  "Missing Closing parentheses to opening parentheses at position: " + str(
                                      self._op_stack[index].get_token_pos()[0])))
        else:
            while len(self._op_stack) != 0:
                self._output_lst.append(self._op_stack.pop())

    def _check_precedence(self, op_token1: Operator, op_token2: Operator) -> float:
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
        Clear the used values so I can convert another expression
        """
        self._op_stack = []
        self._output_lst = []
        self._signed_minus_indexes = []

    def _check_operator_placement(self, cur_index: int, token_list: list):
        """
        This func will check if an operator is placed in a valid way based on its placement and add an error if needed
        :param cur_index:
        :param token_list:
        """
        if self._hit_missing_operands_error and token_list[cur_index].get_token_value().get_placement() == "mid":
            self._hit_missing_operands_error = False
            return
        current_token = token_list[cur_index]
        current_token_placement = current_token.get_token_value().get_placement()
        check_funcs_dict = {
            "left": self._check_left_op,
            "right": self._check_right_op,
            "mid": self._check_mid_op,
        }
        func = check_funcs_dict[current_token_placement]
        is_good, error_dir = func(cur_index, token_list)
        if not is_good:
            if current_token_placement == "mid":
                # missing operands for mid placed operator
                self._error_handler.add_error(
                    BaseCalcError("Missing_Operands_Error",
                                  f"Missing operands for: {current_token.get_token_type()} "
                                  f"at position: {current_token.get_token_pos()[0]}"))

                if cur_index + 1 < len(token_list):
                    next_token = token_list[cur_index + 1].get_token_value()
                    if isinstance(next_token, Operator) and next_token.get_placement() == "mid":
                        self._hit_missing_operands_error = True
            else:
                token_value = current_token.get_token_value().get_op_value()
                token_pos = current_token.get_token_pos()[0]
                self._handle_unary_op_errors(cur_index, token_list, current_token_placement,
                                             token_value, token_pos, error_dir)

    def _handle_unary_op_errors(self, cur_index: int, token_list: list, current_token_placement: str,
                                current_token_value: str, current_pos: int, error_direction: str):
        """
        Func that handles the unary op errors (missing operands / invalid placement)
        :param cur_index:
        :param token_list:
        :param current_token_placement:
        :param current_token_value:
        :param current_pos:
        """
        if self._check_has_error_token(cur_index, token_list, current_token_placement):
            has_after = token_list[cur_index - 1] is not None if current_token_placement == "right" else \
                token_list[cur_index + 1] is not None
            error_token = token_list[cur_index - 1] if error_direction == "after" else token_list[cur_index + 1]
            # add error for invalid use of unary operator
            if has_after:
                self._error_handler.add_error(BaseCalcError("Invalid_Unary_Usage_Error",
                                                            f"Invalid usage of: {current_token_value} "
                                                            f"at position: {current_pos} "
                                                            f"cannot come {error_direction}: "
                                                            f"{error_token.get_token_type()}"))
        else:
            # missing op error for unary operator
            self._error_handler.add_error(
                BaseCalcError("Missing_Operand_Error",
                              f"Missing operand for: {current_token_value} at position: {current_pos}"))

    def _check_has_error_token(self, cur_index: int, token_list: list, placement: str) -> bool:
        """
        Func that returns if there is a next token or before token based on the token's placement
        :param cur_index:
        :param token_list:
        :param placement:
        """
        if placement == "left":
            return cur_index + 1 < len(token_list)
        else:
            return cur_index - 1 >= 0

    def _check_left_op(self, cur_index: int, token_list: list) -> tuple:
        """
        Func to check the validity of a left sided operator
        :param cur_index:
        :param token_list:
        :return: False if non valid, else true
        """
        cur_value = token_list[cur_index].get_token_value()
        next_token, prev_token = self._get_next_and_prev_tokens(cur_index, token_list)
        # first check the more fatal error of having no next token (no operand)
        if next_token is None:
            return False, "None"
        # after checking that there is another token check if it is a valid token
        next_type = next_token.get_token_type()
        if isinstance(cur_value, ILeftSidedOp):
            # unary left sided ops can only come before a unary minus a number or an open paren
            if next_type not in ("U-", "Number", "("):
                return False, "before"
            # there cant be a number a closing paren or a right sided unary op before a left sided unary op
            elif self._check_prev_token(prev_token, ("Number", ")")):
                return False, "after"
            return True, "None"
        # this is used for the binary ops
        return self._check_next_token(next_token, ("Number", "(")), "None"

    def _check_right_op(self, cur_index: int, token_list: list) -> tuple:
        """
        Func to check the validity of a right sided operator
        :param cur_index:
        :param token_list:
        :return: False if non valid, else true
        """
        next_token, prev_token = self._get_next_and_prev_tokens(cur_index, token_list)
        cur_value = token_list[cur_index].get_token_value()
        if prev_token is None:
            return False, "None"
        prev_type = prev_token.get_token_type()
        prev_value = prev_token.get_token_value()
        if isinstance(cur_value, IRightSidedOp):
            # unary right sided operators can come after a number a closing paren or another right sided unary op
            if prev_type not in ("Number", ")") and not isinstance(prev_value, IRightSidedOp):
                return False, "after"
            # there cant be a number a opening paren or a left sided unary op after a right sided unary op
            elif self._check_next_token(next_token, ("Number", "(")):
                return False, "before"
            return True, "None"
        # this is used for the binary ops
        return self._check_prev_token(prev_token, ("Number", ")")), "after"

    def _check_prev_token(self, prev_token: Token, valid_token_values: tuple) -> bool:
        """
        Func that checks if the prev token is valid (in the valid token values or is an instance of a right sided op)
        :param prev_token:
        :param valid_token_values:
        :return: True if valid False if not
        """
        if prev_token is None:
            return False
        prev_type = prev_token.get_token_type()
        prev_value = prev_token.get_token_value()
        return prev_type in valid_token_values or isinstance(prev_value, IRightSidedOp)

    def _check_next_token(self, next_token: Token, valid_token_values: tuple) -> bool:
        """
        Func that checks if the next token is valid (in the valid token values or is an instance of a left sided op)
        :param next_token:
        :param valid_token_values:
        :return:
        """
        if next_token is None:
            return False
        next_type = next_token.get_token_type()
        next_value = next_token.get_token_value()
        return next_type in valid_token_values or isinstance(next_value, ILeftSidedOp)

    def _get_next_and_prev_tokens(self, cur_index: int, token_list: list) -> tuple:
        """
        Func that gets the values of the prev and next token
        :param cur_index:
        :param token_list:
        :return: the values of the tokens or None
        """
        prev_token = token_list[cur_index - 1] if cur_index - 1 >= 0 else None
        next_token = token_list[cur_index + 1] if cur_index + 1 < len(token_list) else None
        return next_token, prev_token

    def _check_mid_op(self, cur_index: int, token_list: list) -> tuple:
        """
        Func that checks the validity of an operator that is binary
        :param cur_index:
        :param token_list:
        :return: False if non valid, else true
        """
        return (self._check_right_op(cur_index, token_list)[0] and
                self._check_left_op(cur_index, token_list)[0]), "None"

    def _check_for_sign_minus(self, cur_index: int, token_list: list) -> bool:
        """
        Func to check if a unary minus is a sign minus
        A sign minus is the highest precedence op and must be pushed before anything else
        :param cur_index:
        :param token_list:
        :return: True if it is a sign minus, False if it isn't
        """
        cur_type = token_list[cur_index].get_token_type()
        if cur_type != "U-":
            return False
        # if the prev minus was a signed one the current one is as well
        if cur_index != 0 and (cur_index - 1) in self._signed_minus_indexes:
            self._signed_minus_indexes.append(cur_index)
            return True
        # token is U-
        prev_token = token_list[cur_index - 1] if cur_index - 1 >= 0 else None
        if prev_token is None or prev_token.get_token_type() == "(" or prev_token.get_token_type() == "U-":
            return False
        self._signed_minus_indexes.append(cur_index)
        return True
