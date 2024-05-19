from typing import List

from sympy import Array, ImmutableDenseNDimArray, Equality, Symbol, derive_by_array, Matrix

from Core.MinimizerCalculator import MinimizerCalculator
from config import PRECISION


class NewtonRaphsonCalculator(MinimizerCalculator):
    gradientEq: ImmutableDenseNDimArray
    hessianEq: List[ImmutableDenseNDimArray]

    def __init__(self, equation: Equality, variables: List[Symbol]):
        super().__init__(equation, variables)
        self.gradientEq = derive_by_array(self.equation, self.variables)
        self.hessianEq = [derive_by_array(i, self.variables) for i in self.gradientEq]

    def calculate(self, position: Array) -> Array | None:
        evaluateGradient = self.evaluateGradient(position)
        evaluateHessian = self.evaluateHessian(position)
        if evaluateHessian.det() == 0:
            return None
        try:
            deltaPosition = evaluateHessian.inv() * Matrix(evaluateGradient)
        except:
            return None
        return position - Array(deltaPosition.transpose().tolist()[0])

    def evaluateGradient(self, position: Array) -> Array:
        return Array(
            [self.gradientEq[i].evalf(subs={self.variables[x]: position[x] for x in range(len(position))}, n=PRECISION)
             for i in
             range(len(position))])

    def evaluateHessian(self, position: Array) -> Matrix:
        return Matrix([[self.hessianEq[i][j].evalf(subs={self.variables[x]: position[x] for x in range(len(position))},
                                                   n=PRECISION)
                        for i in range(len(position))] for j in range(len(position))])

    def clear(self):
        pass
