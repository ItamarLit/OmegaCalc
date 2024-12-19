class BaseCalcError:
    """
    Base error class used to hold the error msg
    """

    def __init__(self, error_type, error_msg):
        self._error_msg = error_msg
        self._error_type = error_type

    def get_msg(self) -> str:
        """
        :return: returns the error msg
        """
        return self._error_msg

    def get_error_type(self):
        """
        :return: returns the error type
        """
        return self._error_type

    def __str__(self):
        return f"Error: {self._error_msg}"


class InvalidFactorialError(Exception):
    """
    Class for the invalid factorial attempt error
    """
    pass


class LargeNumberError(Exception):
    """
    Class for the large number error
    """
    pass


class SmallNumberError(Exception):
    """
    Class for the small number error
    """
    pass


class InvalidHashError(Exception):
    """
    Class for the negative hash attempt error
    """
    pass


class InvalidPowerError(Exception):
    """
    Class for the invalid power attempt error
    """
    pass


class PowerOverflowError(Exception):
    """
    Class for the power overflow error
    """
    pass
