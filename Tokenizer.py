from ErrorHandler import ErrorHandler
from Errors import LexicalError
from Operators import OpData


class Tokenizer:
    """
    This class will check the input for invalid chars and will remove spaces
    The errors will be saved, possible errors in this state:
    1. Invalid chars used in expression ie any char that is not in the valid tokens string
    2. Invalid Number format in expression ie 1234.. or 123.
    3. Invalid usage of an operator ie an op that can start or end the exp
    """

    def __init__(self, error_handler: ErrorHandler):
        # string of all valid chars
        self._valid_tokens = "1234567890.+-*/&^%$@~!()"
        # list to hold all tokens, valid and invalid
        self._token_list = []
        # pattern for all valid numbers
        self._number_pattern = "1234567890."
        # dict to hold operator and token type values except for minus
        self._errors = {"Invalid_Chars_Error": "Invalid Chars found: ",
                        "Invalid_Char_Error": "Invalid Char found: ",
                        "Number_Error": "Invalid Number Format: ",
                        "Empty_Input_Error": "Invalid Input, The input must contain an expression",
                        "Invalid_Usage": "Invalid Operator usage: ",
                        }
        self._invalid_start_pattern = "+*/&^%$@!)"
        self._invalid_end_pattern = "~@$%^&*(-+"
        self._error_handler = error_handler
        # func dict to handle all the input types
        self._funcs_dict = {
            "Number": self._handle_number,
            "Operator": self._handle_operator,
            "Paren": self._handle_paren,
            "Invalid_Char": self._handle_invalid_char,
        }

    def tokenize_expression(self, exp):
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
                        LexicalError(self._errors[current_token_type] + current_token_value,
                                     (starting_index, cur_pos)))
                cur_pos += 1
        else:
            # add an empty input error
            self._error_handler.add_error(LexicalError(self._errors["Empty_Input_Error"], (-1, -1)))
        # handle invalid operators at the start and end of the token list
        self._handle_invalid_operators()
        # check if we need to show errors
        self._error_handler.check_errors()

    def _get_cur_char_type(self, char) -> str:
        if char in self._number_pattern:
            return "Number"
        elif char in OpData.get_op_keys():
            return "Operator"
        elif char in "()":
            return "Paren"
        else:
            return "Invalid_Char"

    def _handle_number(self, cleaned_exp, cur_pos):
        """
        Func that handles the number tokens
        :param cleaned_exp:
        :param cur_pos:
        :return: current_token_value, current_token_type, cur_pos
        """
        current_token_value, cur_pos = self._get_number_token(cleaned_exp, cur_pos)
        # check if the number was valid
        current_token_type = self._check_number(current_token_value)
        return current_token_value, current_token_type, cur_pos

    def _handle_operator(self, cleaned_exp, cur_pos):
        """
        Func to handle the operator tokens
        :param cleaned_exp:
        :param cur_pos:
        :return: current_token_value, current_token_type, cur_pos
        """
        char = cleaned_exp[cur_pos]
        if char == '-':
            # check if the minus is unary or not
            current_token_value = self._check_unary_minus()
            current_token_type = current_token_value
        else:
            current_token_value = char
            current_token_type = char
        current_token_value = OpData.get_op_class(current_token_value)
        return current_token_value, current_token_type, cur_pos

    def _handle_paren(self, cleaned_exp, cur_pos):
        """
        Func to handle the paren tokens
        :param cleaned_exp:
        :param cur_pos:
        :return: current_token_value, current_token_type, cur_pos
        """
        return cleaned_exp[cur_pos], cleaned_exp[cur_pos], cur_pos

    def _get_number_token(self, cleaned_exp: str, starting_index: int):
        """
        :param cleaned_exp:
        :param starting_index:
        :return: returns the number token, this is not yet a checked valid number, also returns the next index to start from
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
        :param number_value:
        :return: checks if the number is of valid form
        """
        if number_value.count('.') <= 1 and not number_value.startswith('.') and not number_value.endswith('.'):
            return "Number"
        return "Number_Error"

    def get_tokens(self):
        return self._token_list

    def clear_tokens(self):
        self._token_list = []

    def _check_unary_minus(self):
        """
        :return: check if the minus is unary or binary
        """
        if len(self._token_list) == 0 or (
                self._token_list[-1].get_token_type() not in ["Number", "Open_Paren"] and
                not isinstance(self._token_list[-1].get_token_value(), type(OpData.get_op_class('!')))
        ):
            return "U-"
        else:
            return '-'

    def _handle_invalid_char(self, cleaned_exp, cur_pos):
        """
        :param cleaned_exp:
        :param cur_pos:
        :return: Handles the invalid char errors
        """
        current_token_type = "Invalid_Char_Error"
        current_token = cleaned_exp[cur_pos]
        cur_pos += 1

        while cur_pos < len(cleaned_exp) and cleaned_exp[cur_pos] not in self._valid_tokens:
            current_token_type = "Invalid_Chars_Error"
            current_token += cleaned_exp[cur_pos]
            cur_pos += 1
        cur_pos -= 1
        return current_token, current_token_type, cur_pos

    def _handle_invalid_operators(self):
        """
        This func will add errors to the error handler if the starting op or the ending op are invalid in their context
        :return:
        """
        if self._token_list:
            # check first token
            first_token = self._token_list[0]
            last_token = self._token_list[-1]
            if first_token.get_token_type() in self._invalid_start_pattern:
                self._error_handler.add_error(
                    LexicalError(self._errors["Invalid_Usage"] + first_token.get_token_type(),
                                 first_token.get_token_pos()))
            # check last token
            if last_token.get_token_type() in self._invalid_end_pattern:
                self._error_handler.add_error(
                    LexicalError(self._errors["Invalid_Usage"] + last_token.get_token_type(),
                                 last_token.get_token_pos()))


class Token:
    """
    This class is used to hold information about the different tokens
    """

    def __init__(self, token_type: str, token_value: str, starting_index: int, ending_index: int):
        self._token_type = token_type
        self._token_value = token_value
        self._starting_index = starting_index
        self._ending_index = ending_index

    def __str__(self):
        return f"Token_type: {self._token_type} , Token_value: {self._token_value} , Token starts at: {self._starting_index} and ends at: {self._ending_index}"

    def get_token_value(self):
        return self._token_value

    def get_token_type(self):
        return self._token_type

    def get_token_pos(self):
        return self._starting_index, self._ending_index
