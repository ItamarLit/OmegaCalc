from Converter import Converter
from ErrorHandler import ErrorHandler
from Tokenizer import Tokenizer
from Evaluator import Evaluator
from OutputHandler import OutputHandler


class CalcHandler:
    """
    This class runs the calc it is only created once in main and ran by using run_calc
    """

    def run_calc(self):
        """
        This is the main func in the class that handles the running of the calculator
        """
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
                self._run_exp(input_exp, tokenizer, converter, evaluator, error_handler)
                self._clear_values(tokenizer, converter, evaluator, error_handler)

    def _run_exp(self, input_exp, tokenizer, converter, evaluator, error_handler):
        """
        This func is called in the run calc and inits all the parts for the calc and
        if any errors are encountered they are shown and the calc process stops and waits for the next exp
        :param input_exp:
        :param tokenizer:
        :param converter:
        :param evaluator:
        :param error_handler:
        """
        try:
            tokenizer.tokenize_expression(input_exp)
            converter.convert(tokenizer.get_tokens())
            evaluator.eval(converter.get_post_fix())
            OutputHandler.output_data(evaluator.get_final())
        except StopIteration:
            # if we get a stopIteration then we had an error and we show all the errors
            error_handler.show_errors()

    def _clear_values(self, tokenizer, converter, evaluator, error_handler):
        """
        Func to clear all the old values in the calculator parts
        :param evaluator:
        :param tokenizer:
        :param converter:
        :param error_handler:
        """
        tokenizer.clear_tokens()
        error_handler.clear_errors()
        converter.clear_converter()
        evaluator.clear_evaluator()
