from MathphiLang.MathLiterals.Expr import Expr
from MathphiLang.Core.Token import Token
from MathphiLang.Core.TokenType import TokenType
from MathphiLang.Operations.Simplify import Simplify, SimplifyArithmetic
from MathphiLang.Solver.Solution import Solution
from MathphiLang.Core.DataSet import Explainer
from MathphiLang.Core.DataSet import Langs
from sympy import sympify
from sympy.printing import print_tree
from sympy.parsing.latex import parse_latex
from sympy import srepr
from sympy.core.add import Add
from sympy.core.mul import Mul

t = Token(TokenType.EXPR, r'1+(-2/3+(1/2+3/4))*12')
expr = Expr(t)
expr.parse()
#print(srepr(expr.parsed_latex))
#expr = sympify('(1^(5/2))',evaluate=False)
#print(srepr(expr))
exp = Explainer(lang = Langs.Egypt )
exp.load(r'E:\MathphiLang\MathDescriptions.xml')
s = SimplifyArithmetic(expr.parsed_latex,exp)
for i in s.getSolution.sequence:
    print(i)


#exp = Explainer()
#exp.load(r'E:\MathphiLang\MathDescriptions.xml')
#exp.extractArithmeticDes()
#print(str(exp.explainArithmetic('addition','numbers','brief',r'$12$',r'$\frac{1}{2}$')))
