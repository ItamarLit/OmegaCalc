from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import pow
from Errors import NegativeFactorialError


@dataclass
class Operator(ABC):
    """
    Abstract operator data class for all the same funcs in all the operators
    """
    _precedence: int
    _value: str
    _description: str

    def get_precedence(self) -> int:
        return self._precedence

    def get_op_value(self) -> str:
        return self._value

    def get_description(self) -> str:
        return self._description


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
        return pow(num1, num2)


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


class UMinus(IUnaryOperator, Operator):
    """
    Class for the unary minus
    """

    def unary_evaluate(self, num1: float) -> float:
        return num1 * -1


class Factorial(IUnaryOperator, Operator):
    """
    Class for the ! op
    """

    def unary_evaluate(self, num1: float) -> float:
        factorial = 1
        if num1 < 0:
            raise NegativeFactorialError("Cannot perform factorial on a negative number")
        elif num1 > 0:
            for i in range(1, int(num1 + 1)):
                factorial = factorial * i
        return factorial


class Negative(IUnaryOperator, Operator):
    """
    Class for the ~ op
    """

    def unary_evaluate(self, num1: float) -> float:
        return num1 * -1


class OpData(ABC):
    """
    Static Class to handle the operator data
    """
    operatorData = {
        '+': Plus(1, '+', "This operator adds two operands"),
        '-': Minus(1, '-', "This operator subtracts two operands"),
        '*': Multiplication(2, '*', "This operator multiplies two operands"),
        '/': Division(2, '/', "This operator divides two operands"),
        '&': Min(6, '&', "This operator gives the minimum between two operands"),
        '^': Power(4, '^', "This operator is the power operator"),
        '%': Modulo(5, '%', "This operator is the modulo operator"),
        '$': Max(6, '$', "This operator gives the maximum between two operands"),
        '@': Avg(6, '@', "This operator gives the average between two operands"),
        '!': Factorial(7, '!', "This operator returns the factorial of a a single un-negative operand"),
        '~': Negative(7, '~', "This is the negative operator"),
        'U-': UMinus(3, '-', "This is the unary minus operator it turns the sign of a given value to the negative of the current sign")
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
