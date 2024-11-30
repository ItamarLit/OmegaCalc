from ErrorHandler import *
from Converter import Converter
from Tokenizer import Tokenizer


def main():
    error_handler = ErrorHandler()
    tokenizer = Tokenizer(error_handler)
    converter = Converter(error_handler)
    while True:
        input_expression = input("Enter an expression: ")
        tokenizer.tokenize_expression(input_expression)
        if error_handler.has_errors():
            error_handler.show_errors()
        else:
            for token in tokenizer.get_tokens():
                print(token)
            converter.convert(tokenizer.get_tokens())
            tokenizer.clear_tokens()
            print(converter.get_rpn())


if __name__ == '__main__':
    main()