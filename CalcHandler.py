from CalcParts.Converter import Converter
from ErrorParts.ErrorHandler import ErrorHandler
from CalcParts.Tokenizer import Tokenizer
from CalcParts.Evaluator import Evaluator
from CalcParts.OutputHandler import OutputHandler


class CalcHandler:
    """
    This class runs the calc it is only created once in main and ran by using run_calc
    """

    def __init__(self):
        self._error_handler = ErrorHandler()
        self._tokenizer = Tokenizer(self._error_handler)
        self._converter = Converter(self._error_handler)
        self._evaluator = Evaluator(self._error_handler)

    def run_calc(self):
        """
        This is the main func in the class that handles the running of the calculator
        """
        try:
            # print the instructions
            OutputHandler.output_main_instructions()
            while True:
                input_exp = input("Enter an expression: ")
                if input_exp.lower() == "exit":
                    print("The program was closed, goodbye")
                    break
                elif input_exp.lower() == "op":
                    OutputHandler.output_op_data()
                else:
                    result, error_list = self.run_single_exp(input_exp)
                    if error_list:
                        self._error_handler.show_errors()
                    else:
                        OutputHandler.output_data(result)
        except KeyboardInterrupt:
            print("\nThe program was forcefully closed, goodbye")
        except EOFError:
            print("\nThe program was forcefully closed, goodbye")

    def run_single_exp(self, input_exp):
        """
        This func runs a single expression through the calculator and returns the final result or the
        errors it encountered
        :return: returns the final value or the errors the calc ran into
        """
        # clear the prev values
        self._clear_values()
        try:
            self._tokenizer.tokenize_expression(input_exp)
            self._converter.convert(self._tokenizer.get_tokens())
            self._evaluator.eval(self._converter.get_post_fix())
            return self._evaluator.get_final(), None
        except StopIteration:
            # if we get a stopIteration then we had an error and we show all the errors
            errors = self._error_handler.get_errors()
            return None, errors

    def _clear_values(self):
        """
        Func to clear all the old values in the calculator parts
        """
        self._tokenizer.clear_tokenizer()
        self._error_handler.clear_errors()
        self._converter.clear_converter()
        self._evaluator.clear_evaluator()
