from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import pow
from Errors import InvalidFactorialError, InvalidHashError


@dataclass
class Operator(ABC):
    """
    Abstract operator data class for all the same funcs and data in all the operators
    """
    _precedence: float
    _value: str
    _placement: str
    _description: str

    def get_precedence(self) -> float:
        return self._precedence

    def get_op_value(self) -> str:
        return self._value

    def get_description(self) -> str:
        return self._description

    def get_placement(self) -> str:
        return self._placement


class IBinaryOperator(ABC):
    """
    Binary operator interface
    """

    @abstractmethod
    def binary_evaluate(self, num1: float, num2: float) -> float:
        pass


class IUnaryOperator(ABC):
    """
    Unary operator interface
    """

    @abstractmethod
    def unary_evaluate(self, num1: float) -> float:
        pass


class ILeftSidedOp(ABC):
    """
    Marker interface for the ops that come to the left of a value
    """


class IRightSidedOp(ABC):
    """
    Marker interface for the ops that come to the right of a value
    """


class Plus(IBinaryOperator, Operator):
    """
    Class for the + op
    """

    def binary_evaluate(self, num1: float, num2: float) -> float:
        return num1 + num2


class Minus(IBinaryOperator, Operator):
    """
    Class for the - op
    """

    def binary_evaluate(self, num1: float, num2: float) -> float:
        return num1 - num2


class Multiplication(IBinaryOperator, Operator):
    """
    Class for the * op
    """

    def binary_evaluate(self, num1: float, num2: float) -> float:
        return num1 * num2


class Division(IBinaryOperator, Operator):
    """
    Class for the / op
    """

    def binary_evaluate(self, num1: float, num2: float) -> float:
        return num1 / num2


class Power(IBinaryOperator, Operator):
    """
    Class for the ^ op
    """
    def binary_evaluate(self, num1: float, num2: float) -> float:
        if num2 <= 0 or num2 < 100 or num1 < 100:
            return pow(num1, num2)
        else:
            num1 = int(num1)
            num2 = int(num2)
            return num1 ** num2


class Max(IBinaryOperator, Operator):
    """
    Class for the $ op
    """

    def binary_evaluate(self, num1: float, num2: float) -> float:
        return num1 if num1 > num2 else num2


class Min(IBinaryOperator, Operator):
    """
    Class for the & class
    """

    def binary_evaluate(self, num1: float, num2: float) -> float:
        return num1 if num1 < num2 else num2


class Modulo(IBinaryOperator, Operator):
    """
    Class for the % op
    """

    def binary_evaluate(self, num1: float, num2: float) -> float:
        return num1 % num2


class Avg(IBinaryOperator, Operator):
    """
    Class for the @ op
    """

    def binary_evaluate(self, num1: float, num2: float) -> float:
        return (num1 + num2) / 2


class UMinus(IUnaryOperator, Operator, ILeftSidedOp):
    """
    Class for the unary minus
    """

    def unary_evaluate(self, num1: float) -> float:
        return num1 * -1


class Factorial(IUnaryOperator, Operator, IRightSidedOp):
    """
    Class for the ! op
    """

    def unary_evaluate(self, num1: int) -> int:
        factorial = 1
        # check for non positive number and non int number
        if num1 < 0 or num1 % 1 != 0:
            raise InvalidFactorialError("Cannot perform factorial on invalid number")
        elif num1 > 0:
            for i in range(1, int(num1 + 1)):
                factorial = factorial * i
        return factorial


class Negative(IUnaryOperator, Operator, ILeftSidedOp):
    """
    Class for the ~ op
    """

    def unary_evaluate(self, num1: float) -> float:
        return num1 * -1


class Hash(IUnaryOperator, Operator, IRightSidedOp):
    """
    Class for the hash op
    """
    def unary_evaluate(self, num1: float) -> float:
        output = 0
        if num1 < 0:
            raise InvalidHashError("Invalid negative hash")
        for char in str(num1):
            if char != '.':
                output = output + int(char)
        return output


class OpData(ABC):
    """
    Static Class to handle the operator data
    """
    operatorData = {
        '+': Plus(1, '+', "mid", "This operator adds two operands"),
        '-': Minus(1, '-', "mid", "This operator subtracts two operands"),
        '*': Multiplication(2, '*', "mid", "This operator multiplies two operands"),
        '/': Division(2, '/', "mid", "This operator divides two operands"),
        '&': Min(5, '&', "mid", "This operator gives the minimum between two operands"),
        '^': Power(3, '^', "mid", "This operator is the power operator"),
        '%': Modulo(4, '%', "mid", "This operator is the modulo operator"),
        '$': Max(5, '$', "mid", "This operator gives the maximum between two operands"),
        '@': Avg(5, '@', "mid", "This operator gives the average between two operands"),
        '!': Factorial(6, '!', "right", "This operator returns the factorial of a a single un-negative operand"),
        '~': Negative(6, '~', "left", "This is the negative operator"),
        '#': Hash(6, '#', "right", "This operator combines the digits of a positive number"),
        'U-': UMinus(2.5, '-', "left",
                     "This is the unary minus operator it turns the sign of a given value to the negative of the current sign")
    }

    @staticmethod
    def get_op_keys():
        return OpData.operatorData.keys()

    @staticmethod
    def get_op_classes():
        return OpData.operatorData.items()

    @staticmethod
    def get_op_class(op_key):
        return OpData.operatorData[op_key]
