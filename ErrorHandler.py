from Errors import BaseCalcError


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

        :return: Prints all the errors to the CLI
        """
        for error in self._errorList:
            print(error + "\n")

    def clear_errors(self):
        """

        :return: Removes all the errors from the error list
        """
        self._errorList = []
