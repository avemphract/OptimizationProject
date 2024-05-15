from typing import List

from sympy import Array

from Core.MinimizerCalculator import MinimizerCalculator
import numpy as np
import matplotlib.pyplot as plt

import time

class EquationSolver:
    minimizer: MinimizerCalculator
    stepSize: int
    position: [Array]
    name: str
    evaluation: [float]
    timePassed: [float]

    def __init__(self, minimizer: MinimizerCalculator, stepSize: int, initialPosition: List[float], name: str):
        self.minimizer = minimizer
        self.stepSize = stepSize
        self.name = name
        self.position = [Array(initialPosition)]
        self.evaluation = [minimizer.evaluateEq(initialPosition)]
        self.timePassed = []

    def calculate(self):
        for i in range(self.stepSize):
            start = time.time()
            result = self.minimizer.calculate(self.position[-1])
            if result is None:
                break
            self.timePassed.append(time.time() - start)
            self.position.append(result)
            self.evaluation.append(self.minimizer.evaluateEq(result))
            if self.evaluation[-1] < 0.0001:
                break

    def evaluationPlot(self):
        xpoints = np.array([i for i in range(len(self.evaluation))])
        ypoints = np.array([self.evaluation[i] for i in range(len(self.evaluation))])
        plt.plot(xpoints, ypoints, label=self.name)

    def deltaEvaluationPlot(self):
        xpoints = np.array([i for i in range(len(self.evaluation) - 1)])
        ypoints = np.array([abs(self.evaluation[i] - self.evaluation[i + 1]) for i in range(len(self.evaluation) - 1)])
        plt.plot(xpoints, ypoints, label=self.name)

    def maxTime(self):
        return max(self.timePassed)

    def minTime(self):
        return min(self.timePassed)

    def averageTime(self):
        return sum(self.timePassed) / len(self.timePassed)

    def getStep(self, error: float):
        for i in range(len(self.evaluation)):
            if self.evaluation[i] < error:
                return i
        return None

    def print(self):
        print(self.name)
        print("step: " + str(len(self.position)))
        print("x :" + str(self.position[-1]))
        print("ev :" + str(self.evaluation[-1]))