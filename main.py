from Converter import Converter
from ErrorHandler import ErrorHandler
from Tokenizer import Tokenizer


def main():
    error_handler = ErrorHandler()
    tokenizer = Tokenizer(error_handler)
    converter = Converter(error_handler)
    # print the instructions
    print("Welcome to the Omega>Sigit Calc please enter an expression")
    while True:
        input_exp = input("Enter an expression: ")
        if input_exp.lower() == "exit":
            print("Goodbye!")
            break
        run_calc(input_exp, tokenizer, converter, error_handler)
        clear_values(tokenizer, converter, error_handler)


def run_calc(input_exp, tokenizer, converter, error_handler):
    """
    Main calc func to preform all the func on the inputed expression and print the output
    :param input_exp:
    :param tokenizer:
    :param converter:
    :param error_handler:
    :return:
    """
    tokenizer.tokenize_expression(input_exp)
    if error_handler.has_errors():
        error_handler.show_errors()
        return
    converter.convert(tokenizer.get_tokens())
    if error_handler.has_errors():
        error_handler.show_errors()
        return
    print(converter.get_post_fix())


def clear_values(tokenizer, converter, error_handler):
    """
    Func to clear all the old values in the calculator parts
    :param tokenizer:
    :param converter:
    :param error_handler:
    :return:
    """
    tokenizer.clear_tokens()
    error_handler.clear_errors()
    converter.clear_converter()

if __name__ == '__main__':
    main()
