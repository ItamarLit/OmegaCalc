from Converter import Converter
from ErrorHandler import ErrorHandler
from Tokenizer import Tokenizer
from Evaluator import Evaluator
from OutputHandler import OutputHandler


def main():
    run_calc()

def run_calc():
    error_handler = ErrorHandler()
    tokenizer = Tokenizer(error_handler)
    converter = Converter(error_handler)
    evaluator = Evaluator(error_handler)
    # print the instructions
    OutputHandler.output_main_instructions()
    while True:
        input_exp = input("Enter an expression: ")
        if input_exp.lower() == "exit":
            print("GoodBye remember: Omega>Sigit")
            break
        elif input_exp.lower() == "op":
            OutputHandler.output_op_data()
        else:
            run_exp(input_exp, tokenizer, converter, evaluator, error_handler)
            clear_values(tokenizer, converter, evaluator, error_handler)

def run_exp(input_exp, tokenizer, converter, evaluator, error_handler):
    """
    Main calc func to preform all the func on the inputed expression and print the output
    :param evaluator:
    :param input_exp:
    :param tokenizer:
    :param converter:
    :param error_handler:
    :return:
    """
    try:
        tokenizer.tokenize_expression(input_exp)
        converter.convert(tokenizer.get_tokens())
        evaluator.eval(converter.get_post_fix())
        OutputHandler.output_data(evaluator.get_final())
    except StopIteration:
        # if we get a stopIteration then we had an error
        error_handler.show_errors()
    except Exception as e:
        # added an exception catch, this shouldn't happen
        print(e)
        pass


def clear_values(tokenizer, converter, evaluator, error_handler):
    """
    Func to clear all the old values in the calculator parts
    :param evaluator:
    :param tokenizer:
    :param converter:
    :param error_handler:
    :return:
    """
    tokenizer.clear_tokens()
    error_handler.clear_errors()
    converter.clear_converter()
    evaluator.clear_evaluator()


if __name__ == '__main__':
    main()
