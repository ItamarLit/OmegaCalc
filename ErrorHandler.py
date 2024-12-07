from Errors import BaseCalcError
from OutputHandler import OutputHandler


class ErrorHandler:
    def __init__(self):
        self._errorList = []

    def add_error(self, error: BaseCalcError):
        """
        :param error:
        :return: adds the error to the error list
        """
        self._errorList.append(error)

    def has_errors(self):
        """
        :return: True if has any errors else false
        """
        return len(self._errorList) != 0

    def show_errors(self):
        """
        Prints all the errors to the CLI
        """
        self._remove_duplicate_errors()
        for error in self._errorList:
            OutputHandler.output_error(error)

    def _remove_duplicate_errors(self):
        """
        Func that will remove all the duplicate errors if there are any
        This can happen for: 1+(+)+2, the (+) will create a double missing operands error
        :return:
        """
        cleaned_errors = []
        for error in self._errorList:
            found_error = False
            for cleaned_error in cleaned_errors:
                if error.get_msg() == cleaned_error.get_msg():
                    found_error = True
            if not found_error:
                cleaned_errors.append(error)
        self._errorList = cleaned_errors

    def clear_errors(self):
        """
        Func that will clear all the errors
        :return: Removes all the errors from the error list
        """
        self._errorList = []

    def check_errors(self):
        if self.has_errors():
            raise StopIteration
