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

    def tokenize_expresion(self):
        cleaned_exp = self._exp.strip()
        for char in cleaned_exp:
            if char not in self._valid_tokens:
                print(f"Invalid token incounterd: {char}")



def main():
    tokens = Tokenizer(input_expression=input("Enter an expression: "))
    tokens.tokenize_expresion()


if __name__ == '__main__':
    main()