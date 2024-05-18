from typing import List

from sympy import Equality, Symbol, Array

from config import PRECISION


class MinimizerCalculator:
    equation: Equality
    step: int = 0
    variables: List[Symbol]

    def __init__(self, equation: Equality, variables: List[Symbol]):
        self.equation = equation
        self.variables = variables

    def calculate(self, position: Array) -> Array:
        pass;

    def evaluateEq(self, position: Array) -> float:
        return self.equation.evalf(subs={self.variables[x]: position[x] for x in range(len(position))}, n=PRECISION)

    def clear(self):
        pass