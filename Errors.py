from abc import ABC, abstractmethod


class BaseCalcError(ABC):
    """
    Base error class used to hold the main error msg
    """
    def __init__(self, error_msg):
        self._error_msg = error_msg


class LexicalError(BaseCalcError):
    """
    Class for all the errors that happen in the tokenizer
    """
    def __init__(self, error_msg, position):
        super.__init__(error_msg)
        self._error_pos = position

    def __str__(self):
        return f"Lexical Error: {self._error_msg} at position: {self._error_pos}"


class ConversionError(BaseCalcError):
    """
    Class for all the errors that happen in the conversion stage
    """
    def __init__(self, error_msg):
        super.__init__(error_msg)

    def __str__(self):
        return f"Conversion Error: {self._error_msg}"


class EvaluationError(BaseCalcError):
    """
    Class for all the errors that happen in the final evaluation
    """
    def __init__(self, error_msg):
        super.__init__(error_msg)

    def __str__(self):
        return f"Evaluation Error: {self._error_msg}"

