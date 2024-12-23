from ErrorParts.ErrorHandler import ErrorHandler
from ErrorParts.Errors import BaseCalcError
from CalcParts.Operators import OpData, IRightSidedOp


class Tokenizer:
    """
    This class will check the input for invalid chars and will remove spaces, the class will create a list of all the
    inputted tokens.
    The errors will be saved, possible errors in this state:
    1. Invalid chars used in expression (any char that is not in the valid tokens string)
    2. Invalid Number format in expression ie 1234.. or 123.
    3. Invalid Empty expression
    """

    def __init__(self, error_handler: ErrorHandler):
        # string of all valid chars
        self._valid_tokens = "1234567890.+-*/&^%$@~!()#"
        # list to hold all tokens, valid and invalid
        self._token_list = []
        # pattern for all valid numbers
        self._number_pattern = "1234567890."
        # dict to hold operator and token type values except for minus
        self._errors = {"Invalid_Chars_Error": "Invalid Chars found: ",
                        "Invalid_Char_Error": "Invalid Char found: ",
                        "Number_Error": "Invalid Number Format: ",
                        "Empty_Input_Error": "Invalid Input, The input must contain an expression",
                        }
        self._error_handler = error_handler
        # func dict to handle all the input types
        self._funcs_dict = {
            "Number": self._handle_number,
            "Operator": self._handle_operator,
            "Paren": self._handle_paren,
            "Invalid_Char": self._handle_invalid_char,
        }

    def tokenize_expression(self, exp):
        """
        This is the main tokenize func it will create a list of tokens that are in the string
        including error tokens and will catch any errors in the process
        :param exp:
        """
        # remove all white spaces and turn the expression into a list
        cleaned_exp = ''.join(exp.split())
        cur_pos = 0
        # check for an empty expression
        if cleaned_exp:
            while cur_pos != len(cleaned_exp):
                starting_index = cur_pos
                # get the char type and func that handles that type
                char_type = self._get_cur_char_type(cleaned_exp[cur_pos])
                func = self._funcs_dict[char_type]
                # get the data from the handler
                current_token_value, current_token_type, cur_pos = func(cleaned_exp, cur_pos)
                # add the token to the list
                self._token_list.append(Token(current_token_type, current_token_value, starting_index, cur_pos))
                # check if I need to add an error
                if current_token_type in self._errors.keys():
                    self._error_handler.add_error(
                        BaseCalcError(current_token_type, self._errors[current_token_type] + current_token_value))
                cur_pos += 1
        else:
            # add an empty input error
            self._error_handler.add_error(BaseCalcError("Empty_Input_Error", self._errors["Empty_Input_Error"]))
        # check if we need to show errors
        self._error_handler.check_errors()

    def _get_cur_char_type(self, char: str) -> str:
        """
        Func that decides the current token type based on the char
        :param char:
        :return: string that represents the token type
        """
        if char in self._number_pattern:
            return "Number"
        elif char in OpData.get_op_keys():
            return "Operator"
        elif char in "()":
            return "Paren"
        else:
            return "Invalid_Char"

    def _handle_number(self, cleaned_exp: str, cur_pos: int):
        """
        Func that handles the number tokens
        :param cleaned_exp:
        :param cur_pos:
        :return: current_token_value, current_token_type, cur_pos
        """
        starting_pos = cur_pos
        current_token_value, cur_pos = self._get_number_token(cleaned_exp, cur_pos)
        # check if the number was valid
        current_token_type = self._check_number(current_token_value)
        # create the error type if needed
        if current_token_type == "Number_Error":
            current_token_value = \
                self._create_error_msg_with_pos(current_token_value, current_token_type, (starting_pos, cur_pos))
        return current_token_value, current_token_type, cur_pos

    def _handle_operator(self, cleaned_exp: str, cur_pos: int):
        """
        Func to tokenize the different operators, including unary minus
        :param cleaned_exp:
        :param cur_pos:
        :return: current_token_value, current_token_type, cur_pos
        """
        char = cleaned_exp[cur_pos]
        if char == '-':
            # check if the minus is unary or not
            current_token_value = self._check_unary_minus(cleaned_exp, cur_pos)
            current_token_type = current_token_value
        else:
            current_token_value = char
            current_token_type = char
        current_token_value = OpData.get_op_class(current_token_value)
        return current_token_value, current_token_type, cur_pos

    def _handle_paren(self, cleaned_exp: str, cur_pos: int):
        """
        Func to tokenize the parentheses
        :param cleaned_exp:
        :param cur_pos:
        :return: current_token_value, current_token_type, cur_pos
        """
        return cleaned_exp[cur_pos], cleaned_exp[cur_pos], cur_pos

    def _get_number_token(self, cleaned_exp: str, starting_index: int):
        """
        Func that returns the number token, even if it is invalid, this func doesn't check the token
        :param cleaned_exp:
        :param starting_index:
        :return: returns the number token, also returns the next index to start from
        """
        cur_index = starting_index
        current_token = cleaned_exp[cur_index]
        cur_index += 1
        while cur_index < len(cleaned_exp) and cleaned_exp[cur_index] in self._number_pattern:
            current_token += cleaned_exp[cur_index]
            cur_index += 1
        return current_token, cur_index - 1

    def _check_number(self, number_value: str):
        """
        Func that checks the number token to see if it is valid
        :param number_value:
        :return: "Number" if the number token is valid else it returns "Number_Error"
        """
        if number_value.count('.') <= 1 and not number_value.startswith('.') and not number_value.endswith('.'):
            return "Number"
        return "Number_Error"

    def get_tokens(self) -> list:
        """
        Func that returns the token list
        :return: list of tokens
        """
        return self._token_list

    def clear_tokenizer(self):
        """
        Func that clears the used token list
        """
        self._token_list = []

    def _check_unary_minus(self, cleaned_exp: str, cur_pos: int):
        """
        Func that checks if a minus is unary or binary
        :return: minus type
        """
        # make sure that (-) is a binary minus for future error handling
        if len(self._token_list) >= 1 and self._token_list[-1].get_token_type() == '(' and \
                len(cleaned_exp) >= 3 and cleaned_exp[cur_pos + 1] == ')':
            return '-'
        if len(self._token_list) == 0 or (
                self._token_list[-1].get_token_type() not in ["Number", ")"] and
                not isinstance(self._token_list[-1].get_token_value(), IRightSidedOp)):
            return "U-"
        else:
            return '-'

    def _handle_invalid_char(self, cleaned_exp: str, cur_pos: int):
        """
        Func that collects an invalid token and decides the correct error type
        :param cleaned_exp:
        :param cur_pos:
        :return: current_token, current_token_type, cur_pos
        """
        # save the starting pos
        starting_pos = cur_pos
        current_token_type = "Invalid_Char_Error"
        current_token_value = cleaned_exp[cur_pos]
        cur_pos += 1
        while cur_pos < len(cleaned_exp) and cleaned_exp[cur_pos] not in self._valid_tokens:
            current_token_type = "Invalid_Chars_Error"
            current_token_value += cleaned_exp[cur_pos]
            cur_pos += 1
        cur_pos -= 1
        current_token_value = \
            self._create_error_msg_with_pos(current_token_value, current_token_type, (starting_pos, cur_pos))
        return current_token_value, current_token_type, cur_pos

    def _create_error_msg_with_pos(self, token_value: str, error_type: str, error_pos: tuple) -> str:
        """
        This func creates an informative error msg for the invalid chars errors
        :param token_value:
        :param error_type:
        :return: string that represents the ending part of the error msg
        """
        if error_type == "Invalid_Chars_Error" or error_type == "Number_Error":
            token_value += f" ,at position: {error_pos[0]} -> {error_pos[1]}"
        else:
            token_value += f" ,at position: {error_pos[0]}"
        return token_value


class Token:
    """
    This class is used to hold information about the different tokens
    the token value can be a string if the token is a number or parentheses, it can also be an operator class instance
    if the token is an operator
    """

    def __init__(self, token_type: str, token_value, starting_index: int, ending_index: int):
        self._token_type = token_type
        self._token_value = token_value
        self._starting_index = starting_index
        self._ending_index = ending_index

    def __str__(self):
        # used for debugging
        return f"Token_type: {self._token_type} , Token_value: {self._token_value} ," \
               f" Token starts at: {self._starting_index} and ends at: {self._ending_index}"

    def get_token_value(self):
        return self._token_value

    def get_token_type(self):
        return self._token_type

    def get_token_pos(self):
        return self._starting_index, self._ending_index
