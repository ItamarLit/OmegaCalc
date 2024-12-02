from ErrorHandler import *
from Tokenizer import Tokenizer


def main():
    error_handler = ErrorHandler()
    tokenizer = Tokenizer(error_handler)
    input_exp = ""
    # print the instructions
    print("Welcome to the Omega>Sigit Calc please enter an expression")
    while input_exp != "exit":
        input_exp = input("Enter an expression: ")
        if input_exp != "exit":
            tokenizer.tokenize_expression(input_exp)
            if error_handler.has_errors():
                error_handler.show_errors()
            else:
                for token in tokenizer.get_tokens():
                    print(token)
            tokenizer.clear_tokens()
            error_handler.clear_errors()


if __name__ == '__main__':
    main()