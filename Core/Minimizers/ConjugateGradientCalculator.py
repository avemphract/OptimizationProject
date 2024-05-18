from typing import List

import sympy
from sympy import Array, Equality, Symbol, Float

from Core.MinimizerCalculator import MinimizerCalculator
from config import PRECISION, MINIMUM_STEP_SIZE


class ConjugateGradientCalculator(MinimizerCalculator):
    gradientEq: Array
    dk = None
    aPrecesion = 10

    def __init__(self, equation: Equality, variables: List[Symbol]):
        super().__init__(equation, variables)
        self.gradientEq = sympy.derive_by_array(equation, variables)

    def calculate(self, position: Array) -> Array | None:
        gCurrent = self.evaluateGradient(position)
        if gCurrent == [0 for i in range(len(self.variables))]:
            return position
        if self.dk is None:
            self.dk = -gCurrent
        ak = self.calculateStepSize(position, self.dk)
        if ak is None:
            return None
        xNext = position + ak * self.dk
        gNext = self.evaluateGradient(xNext)
        b = self.calculateB(gCurrent, gNext)
        if b is None:
            return None
        self.dk = -gNext + (b * self.dk)
        return xNext

    def calculateB(self, gCurrent, gNext):
        pass;

    def calculateStepSize(self, initialPosition: Array, direction: Array) -> float | None:
        minValue = self.evaluateEq(initialPosition)
        minStep = 0
        deepStep = 0
        while minStep == 0:
            deepStep = deepStep + 1
            prevValue = None
            if MINIMUM_STEP_SIZE > 10:
                return None
            for i in range(self.aPrecesion):
                step = Float((i - 1) / (self.aPrecesion ** deepStep), PRECISION)
                value = self.evaluateEq(initialPosition + direction * Float(step, PRECISION))
                if prevValue == value:
                    return None
                prevValue = value
                if value < abs(minValue):
                    minValue = value
                    minStep = step
            k = 1
        return minStep

    def evaluateGradient(self, position: Array) -> Array:
        return Array(
            [self.gradientEq[i].evalf(subs={self.variables[x]: position[x] for x in range(len(position))}, n=PRECISION)
             for i in
             range(len(position))])

    def clear(self):
        self.dk = None
