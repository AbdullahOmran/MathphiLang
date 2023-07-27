from MathphiLang.MathLiterals.Expr import Expr
from MathphiLang.Core.Token import Token
from MathphiLang.Core.TokenType import TokenType
from MathphiLang.Operations.Simplify import Simplify, SimplifyArithmetic
from MathphiLang.Solver.Solution import Solution
from sympy.printing import print_tree
from sympy.parsing.latex import parse_latex
from sympy import srepr
from sympy.core.add import Add

t = Token(TokenType.EXPR, r'(4+1)/2 +2+3*5 + 2^{3}+2-3*(3/4 - 2/(1+1) +(2-1)^(1-2))')
expr = Expr(t)
expr.parse()
print(srepr(expr.parsed_latex))
#expr = Add(1,2,3,4,5, evaluate=False)
s = SimplifyArithmetic(expr.parsed_latex)
for sol in s.getSolution():
    print(sol)
