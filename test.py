from MathphiLang.MathLiterals.Expr import Expr
from MathphiLang.Core.Token import Token
from MathphiLang.Core.TokenType import TokenType
from MathphiLang.Operations.Simplify import Simplify
from MathphiLang.Solver.Solution import Solution
from sympy.printing import print_tree
from sympy.parsing.latex import parse_latex
t = Token(TokenType.EXPR, r'-5/3+1+3^{2}')
expr = Expr(t)
expr.parse()
sol = Solution()
nodes = []
nodes.append(expr)
s = Simplify(nodes,sol)
print(s.simplify_basic_ops())

    
