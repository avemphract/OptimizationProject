import sympy
from sympy import *

from Core.EquationSolver import EquationSolver
from Core.Minimizers.DaiYuanCalculator import DaiYuanCalculator
from Core.Minimizers.FletcherReevesCalculator import FletcherReevesCalculator
from Core.Minimizers.HestenesStiefelCalculator import HestenesStiefelCalculator
from Core.Minimizers.NewtonRaphsonCalculator import NewtonRaphsonCalculator
from Core.Minimizers.PolakRibiereCalculator import PolakRibiereCalculator
from config import PRECISION, NUMBER_OF_STEPS

x1, x2, x3, x4 = symbols('x_1 x_2 x_3 x_4', real=True)
i = Idx('i', (1, 11))
a = Function('a')
b = Function('b')
A = [0.1957, 0.1947, 0.1735, 0.16, 0.0844, 0.0627, 0.0456, 0.0342, 0.0323, 0.0235, 0.0246]
B = [0.25, 0.50, 1.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0]

eq = sympy.Sum(sympy.Pow(a(i) - ((x1 * (1 + x2 * b(i))) / (1 + x3 * b(i) + x4 * sympy.Pow(b(i), 2))), 2),
               (i, 1, 11)).doit()
eq = eq.replace(a, lambda i: A[i - 1])
eq = eq.replace(b, lambda i: B[i - 1])
var = [x1, x2, x3, x4]

initialPosition1 = [0.3604731246866024, 0.07230024599267677, 0.11897895468122173, 0.045488678141934774]
initialPosition2 = [0.03259413754069159, 0.22363517468946045, 0.3678804141000155, 0.21481580185423677]
initialPosition3 = [0.26529854910838047, 0.1427029905292762, 0.12562171017636237, 0.3589400996677316]
initialPositions = [initialPosition1, initialPosition2, initialPosition3]

h = EquationSolver(HestenesStiefelCalculator(eq, var), NUMBER_OF_STEPS, "Hestenes-Stiefel")

p = EquationSolver(PolakRibiereCalculator(eq, var), NUMBER_OF_STEPS, "Polak-Ribiere")

f = EquationSolver(FletcherReevesCalculator(eq, var), NUMBER_OF_STEPS, "Fletcher-Reeves")

d = EquationSolver(DaiYuanCalculator(eq, var), NUMBER_OF_STEPS, "Dai-Yuan")

n = EquationSolver(NewtonRaphsonCalculator(eq, var), NUMBER_OF_STEPS, "Newton-Raphson")

lis = [h,p,f,d,n]
for j in initialPositions:
        d.calculate(j)
d.print()

#for i in lis:
#    for j in initialPositions:
#        i.calculate(j)
#    i.print()



