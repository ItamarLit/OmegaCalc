class BaseCalcError:
    """
    Base error class used to hold the error msg
    """

    def __init__(self, error_msg):
        self._error_msg = error_msg

    def get_msg(self) -> str:
        """
        :return: returns the error msg
        """
        return self._error_msg

    def __str__(self):
        return f"Error: {self._error_msg}"


class InvalidFactorialError(Exception):
    """
    Class for the negative factorial attempt error
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
