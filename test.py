from MathphiLang.MathLiterals.Expr import Expr
from MathphiLang.Core.Token import Token
from MathphiLang.Core.TokenType import TokenType
from MathphiLang.Operations.Simplify import Simplify, SimplifyArithmetic
from MathphiLang.Solver.Solution import Solution
from MathphiLang.Core.DataSet import Explainer
from sympy.printing import print_tree
from sympy.parsing.latex import parse_latex
from sympy import srepr
from sympy.core.add import Add
from sympy.core.mul import Mul

t = Token(TokenType.EXPR, r'(4+1)/2 +2+3*5 + 2^{3}+2-3*(3/4 - 2/(1+1) +(2-1)^(1-2))')
expr = Expr(t)
expr.parse()
print(srepr(expr.parsed_latex))
#expr = Mul(1,Add(1,1,1,evaluate=False),3,4, evaluate=False)
s = SimplifyArithmetic(expr.parsed_latex)
for sol in s.getSolution:
    print(sol)

#exp = Explainer()
#exp.load(r'E:\MathphiLang\MathDescriptions.xml')
#exp.extractArithmeticDes()
#print(str(exp.explainArithmetic('addition','numbers','brief',r'$12$',r'$\frac{1}{2}$')))
