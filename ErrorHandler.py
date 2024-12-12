from Errors import BaseCalcError
from OutputHandler import OutputHandler


class ErrorHandler:
    """
    Class that handles all error handler funcs, this class will hold a list of the found errors and will be
    able to show the errors to the user by using the OutputHandler
    """

    def __init__(self):
        # this is the error list that will hold all the errors
        self._errorList = []

    def add_error(self, error: BaseCalcError):
        """
        Func that adds an error to the error list
        :param error:
        """
        self._errorList.append(error)

    def has_errors(self) -> bool:
        """
        Func that checks if there are any errors
        :return: True if has any errors else false
        """
        return len(self._errorList) != 0

    def show_errors(self):
        """
        Prints all the errors to the CLI using the output handler
        """
        for error in self._errorList:
            OutputHandler.output_error(error)

    def clear_errors(self):
        """
        Func that will clear all the errors
        """
        self._errorList = []

    def check_errors(self):
        """
        Func that will raise a stop iteration error if there are any errors
        """
        if self.has_errors():
            raise StopIteration

    def get_errors(self):
        """
        Func that returns the contents of the error list
        """
        return self._errorList
