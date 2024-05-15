from typing import List

from sympy import Equality, Symbol, Matrix

from Core.Minimizers.ConjugateGradientCalculator import ConjugateGradientCalculator

class PolakRibiereCalculator(ConjugateGradientCalculator):
    def __init__(self, equation: Equality, variables: List[Symbol]):
        super().__init__(equation, variables)

    def calculateB(self, gCurrent, gNext):
        a = Matrix(gNext).transpose() * Matrix(gNext - gCurrent)
        b = Matrix(gCurrent).transpose() * Matrix(gCurrent)
        return a[0] / b[0]