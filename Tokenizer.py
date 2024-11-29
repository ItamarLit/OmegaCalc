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
        # list of all the possible token types and there chars except for minus
        self._token_types = ["Number", "Plus", "Multiplication", "Division",
                             "Power", "Factorial", "Max", "Min",
                             "Avg", "Negative", "Modulo", "Error"]
        self._number_pattern = "1234567890."
        # dict to hold all the operator precedences
        self.operator_precedence_table = {"+": 1}

    def tokenize_expression(self):
        """

        :return: This func will add tokens to the token list of the tokenizer
        """
        # remove all white spaces
        cleaned_exp = ''.join(self._exp.split())
        current_token = ""
        last_token_type = ""
        for char in cleaned_exp:
            if char not in self._valid_tokens:
                # SWAP TO A BETTER ERROR
                raise ValueError(f"Invalid token incounterd: {char}")
            else:
                # check if the token is a number
                if char in self._number_pattern:
                    pass
                # check if the char is an operator (not including minus)
                elif char in "+*/^%$@!~":
                    pass
                # check if the minus is unary or not
                elif char == '-':
                    pass
                else:
                    # raise an error because the token is not a valid token
                    # this shouldn't happen
                    pass


class Token:
    """
    This class is used to hold information about the different tokens
    """

    def __init__(self, token_type, token_value, token_precedence):
        self._token_type = token_type
        self._token_value = token_value
        self._precedence = token_precedence


def main():
    tokens = Tokenizer(input_expression=input("Enter an expression: "))
    tokens.tokenize_expresion()


if __name__ == '__main__':
    main()
