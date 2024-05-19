from typing import List, Tuple

from IPython.core.display_functions import display
from sympy import Array, Float

from Core.MinimizerCalculator import MinimizerCalculator
import numpy as np
import matplotlib.pyplot as plt

import time


class EquationSolver:
    minimizer: MinimizerCalculator
    stepSize: int
    position: List[List[Array]]
    name: str
    evaluation: List[List[float]]
    timePassed: List[List[float]]

    def __init__(self, minimizer: MinimizerCalculator, stepSize: int, name: str):
        self.minimizer = minimizer
        self.stepSize = stepSize
        self.name = name
        self.timePassed = []
        self.position = []
        self.evaluation = []

    def calculate(self, initialPosition: List[Float]):
        self.minimizer.clear()
        self.position.append([Array(initialPosition)])
        self.evaluation.append([self.minimizer.evaluateEq(initialPosition)])
        self.timePassed.append([])
        for i in range(self.stepSize):
            start = time.time()
            result = self.minimizer.calculate(self.position[-1][-1])
            if result is None:
                break
            self.timePassed[-1].append(time.time() - start)
            self.position[-1].append(result)
            self.evaluation[-1].append(self.minimizer.evaluateEq(result))
            if self.evaluation[-1][-1] < 0.0001:
                break

    def evaluationPlot(self) -> Tuple[List[float], List[float]]:
        x = [];
        y = [];
        for i in range(max(len(j) for j in self.evaluation)):
            x.append(i)
            temp = 0
            tempSize = 0
            for k in range(len(self.evaluation)):
                if len(self.evaluation[k]) > i:
                    temp += self.evaluation[k][i]
                    tempSize += 1
            if tempSize != 0:
                y.append(temp / tempSize)
        return x, y
        #xpoints = np.array([i for i in range(len(self.evaluation[-1]))])
        #ypoints = np.array([self.evaluation[-1][i] for i in range(len(self.evaluation[-1]))])
        #plt.plot(xpoints, ypoints, label=self.name)

    def deltaEvaluationPlot(self) -> Tuple[List[float], List[float]]:
        x = []
        y = []
        for i in range(max(len(j) - 1 for j in self.evaluation)):
            temp = 0
            tempSize = 0
            for k in range(len(self.evaluation)):
                if len(self.evaluation[k]) > i + 1:
                    temp += abs(self.evaluation[k][i] - self.evaluation[k][i + 1])
                    tempSize += 1
            if tempSize != 0:
                x.append(i)
                y.append(temp / tempSize)
        return x, y

    def maxTime(self):
        return max(max(i) for i in self.timePassed)

    def minTime(self):
        return min(min(i) for i in self.timePassed)

    def averageTime(self):
        return sum(sum(i) for i in self.timePassed) / sum(len(i) for i in self.timePassed)

    def totalTime(self):
        return sum(sum(i) for i in self.timePassed)

    def timePlot(self):
        x = []
        y = []
        for i in range(max(len(j) for j in self.timePassed)):
            temp = 0
            tempSize = 0
            for k in range(len(self.timePassed)):
                if len(self.timePassed[k]) > i:
                    temp += self.timePassed[k][i]
                    tempSize += 1
            if tempSize != 0:
                x.append(i)
                y.append(temp / tempSize)
        return x, y

    def getStep(self, error: float):
        results = []
        for i in self.evaluation:
            found = False
            for j in range(len(i)):
                if i[j] < error:
                    results.append(str(j))
                    found = True
                    break
            if not found:
                results.append("-")

        if len(results) == 0:
            return None
        return results

    def print(self):
        print(self.name)
        print("Average time requirement: " + str(self.averageTime()))
        print("Total time requirement: " + str(self.totalTime()))
        print("DeltaPlot: ", str(self.deltaEvaluationPlot()))
        print("Plot: ", str(self.evaluationPlot()))
        for i in range(len(self.position)):
            print(str(i + 1) + ". Calculation")
            print("Step count: " + str(len(self.position[i])))
            print("Calculated X :" + str(self.position[i][-1]))
            print("Calculated evaluation :" + str(self.evaluation[i][-1]))
        print("-----")

    def display(self):
        display(self.name)
        display("Average time requirement: " + str(self.averageTime()))
        display("Total time requirement: " + str(self.totalTime()))
        for i in range(len(self.position)):
            display(str(i + 1) + ". Calculation")
            display("Step count: " + str(len(self.position[i])))
            display("Calculated X :" + str(self.position[i][-1]))
            display("Calculated evaluation :" + str(self.evaluation[i][-1]))
        display("-----")
