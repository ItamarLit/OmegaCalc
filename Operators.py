from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import pow


@dataclass
class Operator(ABC):
    """
    Abstract operator data class for all the same funcs in all the operators
    """
    precedence: int

    def get_precedence(self) -> int:
        return self.precedence


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
        pass


class Negative(IUnaryOperator, Operator):
    """
    Class for the ~ op
    """

    def unary_evaluate(self, num1: float) -> float:
        return num1 * -1


class OpData:
    """
    Class to handle the operator data
    """
    def __init__(self):
        self.__operatorData = {
            '+': Plus(1),
            '-': Minus(1),
            '*': Multiplication(2),
            '/': Division(2),
            '&': Min(6),
            '^': Power(3),
            '%': Modulo(5),
            '$': Max(6),
            '@': Avg(6),
            '!': Factorial(7),
            '~': Negative(7),
            'U-': UMinus(4)
        }