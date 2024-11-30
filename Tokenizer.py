from ErrorHandler import ErrorHandler
from Errors import *


class Tokenizer:
    """
    This class will check the input for invalid chars and will remove spaces
    The errors will be saved, possible errors in this state:
    1. Invalid chars used in expression ie any char that is not in the valid tokens string
    2. Invalid Number format in expression ie 1234.. or 123.
    3. Invalid Starting char ie binary op or !
    4. Invalid Ending char ie binary op or ~ or -
    """

    def __init__(self, error_handler: ErrorHandler):
        # String to hold all valid tokens in the calc
        self._valid_tokens = "1234567890.+-*/&^%$@~!()"
        # list to hold all tokens, valid and invalid
        self._token_list = []
        # pattern for all valid numbers
        self._number_pattern = "1234567890."
        # dict to hold operator and token type values except for minus
        self._operators = {'+': "Plus", '*': "Multiplication", '/': "Division", '^': "Power", '!': "Factorial",
                           '~': "Negative", '@': "Avg", '%': "Modulo", '&': "Min", '$': "Max"}

        self._paren = {'(': "Open_Paren", ')': "Close_Paren"}
        self._errors = {"Invalid_Chars_Error": "Invalid Chars found: ", "Invalid_Char_Error": "Invalid Char found: ",
                        "Number_Error": "Invalid Number Format: ",
                        "Empty_Input_Error": "Invalid Input, The input must contain an expression",
                        "Invalid_Start": "Invalid Starting operator: ", "Invalid_End": "Invalid Ending Operator: "}
        self._invalid_start_pattern = "+*/&^%$@!)"
        self._invalid_end_pattern = "~@$%^&*(-+"

        self._error_handler = error_handler

    def tokenize_expression(self, exp):
        """
        :return: This func will add tokens to the token list of the tokenizer
        """
        # remove all white spaces and turn the expression into a list
        cleaned_exp = ''.join(exp.split())
        # check for an empty expression
        if cleaned_exp:
            current_token = ""
            current_token_type = ""
            last_token_type = ""
            cur_pos = 0

            while cur_pos != len(cleaned_exp):
                starting_index = cur_pos
                char = cleaned_exp[cur_pos]

                # check if the token is a number
                if char in self._number_pattern:
                    current_token, cur_pos = self.get_number_token(cleaned_exp, cur_pos, current_token)
                    # check if the number was valid
                    if self.check_number(current_token):
                        # valid token of type num
                        current_token_type = "Number"
                    else:
                        # invalid token type
                        current_token_type = "Number_Error"

                # check if the char is an operator (not including minus)
                elif char in self._operators.keys():
                    current_token_type = self._operators[char]
                    current_token = char

                # check if the minus is unary or not
                elif char == '-':
                    current_token = char
                    # check for unary minus
                    if last_token_type == "" or (last_token_type != "Close_Paren" and last_token_type != "Number" and last_token_type != "Factorial"):
                        current_token_type = "Unary_Minus"
                        current_token = "U-"
                    else:
                        current_token_type = "Minus"

                # check paren
                elif char in self._paren.keys():
                    current_token = char
                    current_token_type = self._paren[char]

                else:
                    # error because the char is not a valid token
                    current_token_type = "Invalid_Char_Error"
                    current_token += char
                    cur_pos += 1
                    while cur_pos < len(cleaned_exp) and cleaned_exp[cur_pos] not in self._valid_tokens:
                        current_token_type = "Invalid_Chars_Error"
                        current_token += cleaned_exp[cur_pos]
                        cur_pos += 1
                    cur_pos -= 1
                ending_index = cur_pos
                # add the token
                self._token_list.append(Token(current_token_type, current_token, starting_index, ending_index))
                # check if I need to add an error
                if current_token_type in self._errors.keys():
                    self._error_handler.add_error(LexicalError(self._errors[current_token_type] + current_token, (starting_index, ending_index)))
                # reset
                current_token = ""
                cur_pos += 1
                last_token_type = current_token_type
        else:
            # add an empty input error
            self._error_handler.add_error(LexicalError(self._errors["Empty_Input_Error"], (-1, -1)))
        # handle invalid operators at the start and end of the token list
        if self._token_list:
            # check first token
            if self._token_list[0].get_token_value() in self._invalid_start_pattern:
                self._error_handler.add_error(
                    LexicalError(self._errors["Invalid_Start"] + self._token_list[0].get_token_value(), (-1, 0)))
            # check last token
            if self._token_list[-1].get_token_value() in self._invalid_end_pattern:
                self._error_handler.add_error(
                    LexicalError(self._errors["Invalid_End"] + self._token_list[-1].get_token_value(), (-1, 0)))


    def get_number_token(self, cleaned_exp: str, starting_index: int, current_token: str):
        """
        :param cleaned_exp:
        :param starting_index:
        :param current_token:
        :return: returns the number token, this is not yet a checked valid number, also returns the next index to start from
        """
        cur_index = starting_index
        current_token += cleaned_exp[cur_index]
        cur_index += 1
        while cur_index < len(cleaned_exp) and cleaned_exp[cur_index] in self._number_pattern:
            current_token += cleaned_exp[cur_index]
            cur_index += 1
        return current_token, cur_index - 1

    def check_number(self, number_value: str):
        """
        :param number_value:
        :return: checks if the number is of valid form
        """
        if number_value.count('.') <= 1 and not number_value.startswith('.') and not number_value.endswith('.'):
            return True
        return False

    def get_tokens(self):
        return self._token_list

    def clear_tokens(self):
        self._token_list = []

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

