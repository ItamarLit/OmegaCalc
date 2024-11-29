class Tokenizer:
    """
    This class will check the input for invalid chars and will remove spaces
    The errors will be saved, possible errors in this state:
    1. Invalid chars used in expression ie any char that is not in the valid tokens string
    2. Invalid Number format in expression ie 1234.. or 123.
    """

    def __init__(self, input_expression):
        self._exp = input_expression
        # String to hold all valid tokens in the calc
        self._valid_tokens = "1234567890.+-*/&^%$@~!"
        # list to hold all tokens, valid and invalid
        self._token_list = []
        # pattern for all valid numbers
        self._number_pattern = "1234567890."
        # dict to hold all the operator precedences
        self._operator_precedence_table = {"Error": -1, "Number": 0, "Plus": 1, "Minus": 1, "Multiplication": 2,
                                           "Division": 3, "Power": 4, "Unary_Minus": 5,
                                           "Modulo": 6, "Avg": 7, "Max": 7, "Min": 7, "Negative": 8, "Factorial": 8}
        # dict to hold operator and token type values except for minus
        self._operators = {'+': "Plus", '*': "Multiplication", '/': "Division", '^': "Power", '!': "Factorial",
                           '~': "Negative", '@': "Avg", '%': "Modulo", '&': "Min", '$': "Max"}

    def tokenize_expression(self):
        """
        :return: This func will add tokens to the token list of the tokenizer
        """
        # remove all white spaces and turn the expression into a list
        cleaned_exp = ''.join(self._exp.split())
        current_token = ""
        last_token_type = ""
        cur_pos = 0

        while cur_pos != len(cleaned_exp):
            char = cleaned_exp[cur_pos]
            if char not in self._valid_tokens:
                # SWAP TO A BETTER ERROR
                raise ValueError(f"Invalid token incounterd: {char}")
            else:
                # check if the token is a number
                if char in self._number_pattern:
                    current_token += char
                    cur_pos += 1
                    while self.check_number(current_token) and cleaned_exp[cur_pos] in self._number_pattern \
                            and cur_pos != len(cleaned_exp):
                        current_token += cleaned_exp[cur_pos]
                        if cur_pos < len(cleaned_exp) and self.check_number(current_token + cleaned_exp[cur_pos + 1]):
                            cur_pos += 1
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
                    pass
                else:
                    # raise an error because the token is not a valid token
                    # this shouldn't happen
                    last_token_type = "Error"
                # add the token
                self._token_list.append(
                    Token(last_token_type, current_token, self._operator_precedence_table[last_token_type]))
                cur_pos += 1
                current_token = ""

    def check_number(self, number_value):
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

    def __init__(self, token_type, token_value, token_precedence):
        self._token_type = token_type
        self._token_value = token_value
        self._precedence = token_precedence

    def __str__(self):
        return f"Token_type: {self._token_type} , Token_value: {self._token_value} , Token_precedence: {self._precedence}"


def main():
    tokens = Tokenizer(input_expression=input("Enter an expression: "))
    tokens.tokenize_expression()
    for token in tokens.get_tokens():
        print(token)



if __name__ == '__main__':
    main()
