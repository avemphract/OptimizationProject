import sympy
from sympy import *
import random

from Core.EquationSolver import EquationSolver
from Core.Minimizers.DaiYuanCalculator import DaiYuanCalculator
from Core.Minimizers.FletcherReevesCalculator import FletcherReevesCalculator
from Core.Minimizers.HestenesStiefelCalculator import HestenesStiefelCalculator
from Core.Minimizers.NewtonRaphsonCalculator import NewtonRaphsonCalculator
from Core.Minimizers.PolakRibiereCalculator import PolakRibiereCalculator

x1, x2, x3, x4 = symbols('x_1 x_2 x_3 x_4', real=True)
i = Idx('i', (1, 11))
a = Function('a')
b = Function('b')
A = [0.1957, 0.1947, 0.1735, 0.16, 0.0844, 0.0627, 0.0456, 0.0342, 0.0323, 0.0235, 0.0246];
B = [0.25, 0.50, 1.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0]

eq = sympy.Sum(sympy.Pow(a(i) - ((x1 * (1 + x2 * b(i))) / (1 + x3 * b(i) + x4 * sympy.Pow(b(i), 2))), 2),
               (i, 1, 11)).doit()
eq = eq.replace(a, lambda i: A[i - 1])
eq = eq.replace(b, lambda i: B[i - 1])
var = [x1, x2, x3, x4]

initialPosition = [random.random() * 0.42, random.random() * 0.42, random.random() * 0.42, random.random() * 0.42]
stepSize = 10

h = EquationSolver(HestenesStiefelCalculator(eq, var), stepSize, initialPosition, "Hestenes-Stiefel")

p = EquationSolver(PolakRibiereCalculator(eq, var), stepSize, initialPosition, "Polak-Ribiere")

f = EquationSolver(FletcherReevesCalculator(eq, var), stepSize, initialPosition, "Fletcher-Reeves")

d = EquationSolver(DaiYuanCalculator(eq, var), stepSize, initialPosition, "Dai-Yuan")

n = EquationSolver(NewtonRaphsonCalculator(eq, var), stepSize, initialPosition, "Newton-Raphson")

lis = [h, p, f, d, n]

for i in lis:
    i.calculate()
    i.print()



