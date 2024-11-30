class Tokenizer:
    """
    This class will check the input for invalid chars and will remove spaces
    The errors will be saved, possible errors in this state:
    1. Invalid chars used in expression ie any char that is not in the valid tokens string
    2. Invalid Number format in expression ie 1234.. or 123.
    """

    def __init__(self, input_expression: str):
        self._exp = input_expression
        # String to hold all valid tokens in the calc
        self._valid_tokens = "1234567890.+-*/&^%$@~!()"
        # list to hold all tokens, valid and invalid
        self._token_list = []
        # pattern for all valid numbers
        self._number_pattern = "1234567890."
        # dict to hold all the operator precedences
        self._operator_precedence_table = {"Error": -1, "Number": 0, "Plus": 1, "Minus": 1, "Multiplication": 2,
                                           "Division": 3, "Power": 4, "Unary_Minus": 5,
                                           "Modulo": 6, "Avg": 7, "Max": 7, "Min": 7, "Negative": 8,
                                           "Factorial": 8, "Close_Paren": 9, "Open_Paren": 9}
        # dict to hold operator and token type values except for minus
        self._operators = {'+': "Plus", '*': "Multiplication", '/': "Division", '^': "Power", '!': "Factorial",
                           '~': "Negative", '@': "Avg", '%': "Modulo", '&': "Min", '$': "Max"}
        self._paren = {'(': "Open_Paren", ')': "Close_Paren"}

    def tokenize_expression(self):
        """
        :return: This func will add tokens to the token list of the tokenizer
        """
        # remove all white spaces and turn the expression into a list
        cleaned_exp = ''.join(self._exp.split())
        # check for an empty expression
        if cleaned_exp:
            current_token = ""
            last_token_type = ""
            cur_pos = 0
            ending_index = -1
            while cur_pos != len(cleaned_exp):
                starting_index = cur_pos
                char = cleaned_exp[cur_pos]
                # check if the token is a number
                if char in self._number_pattern:
                    current_token, cur_pos = self.get_number_token(cleaned_exp, cur_pos, current_token)
                    # check if the number was valid
                    if self.check_number(current_token):
                        # valid token of type num
                        last_token_type = "Number"
                    else:
                        # invalid token type
                        last_token_type = "Error"
                # check if the char is an operator (not including minus)
                elif char in "+*/^%$@!~":
                    last_token_type = self._operators[char]
                    current_token = char
                # check if the minus is unary or not
                elif char == '-':
                    current_token = char
                    # check for unary minus
                    if last_token_type == "" or (last_token_type != "Close_Paren" and last_token_type != "Number"):
                        last_token_type = "Unary_Minus"
                    else:
                        last_token_type = "Minus"
                # check paren
                elif char in "()":
                    current_token = char
                    last_token_type = self._paren[char]
                else:
                    # error because the char is not a valid token
                    last_token_type = "Error"
                    current_token += char
                    cur_pos += 1
                    while cur_pos < len(cleaned_exp) and cleaned_exp[cur_pos] not in self._valid_tokens:
                        current_token += cleaned_exp[cur_pos]
                        cur_pos += 1
                    cur_pos -= 1
                # the ending index is the last index of cur pos
                ending_index = cur_pos
                # add the token
                self._token_list.append(
                    Token(last_token_type, current_token, self._operator_precedence_table[last_token_type], starting_index,
                          ending_index)
                )
                cur_pos += 1
                current_token = ""
        else:
            self._token_list.append(
                Token("Error", "-1", self._operator_precedence_table["Error"], -1,
                      -1)
            )

    def get_number_token(self, cleaned_exp : str, starting_index: int, current_token: str):
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


class Token:
    """
    This class is used to hold information about the different tokens
    """

    def __init__(self, token_type : str, token_value: str, token_precedence: int, starting_index : int, ending_index : int):
        self._token_type = token_type
        self._token_value = token_value
        self._precedence = token_precedence
        self._starting_index = starting_index
        self._ending_index = ending_index

    def __str__(self):
        return f"Token_type: {self._token_type} , Token_value: {self._token_value} , Token_precedence: {self._precedence} ," \
               f" Token starts at: {self._starting_index} and ends at: {self._ending_index}"


def main():
    tokens = Tokenizer(input_expression=input("Enter an expression: "))
    tokens.tokenize_expression()
    for token in tokens.get_tokens():
        print(token)


if __name__ == '__main__':
    main()
