from .MathLiteral import MathLiteral
from ..Core.Token import Token
from . import MathLiterals
from sympy.parsing.latex import parse_latex
from sympy.core.add import Add
from sympy.core.symbol import Symbol
from sympy.core.mul import Mul
from sympy.core.expr import Expr as Expression
class Expr(MathLiteral):
    def __init__(self,token: Token):
        self.token = token
        self.value = token.value
        self.parsed_latex =''
    def classify(self):
        for literal in MathLiterals:
            method_name = 'is_'+literal.value
            get = getattr(self,method_name,self.method_not_found())
            if get is not None and get():
                return literal.value
        return False
    def is_polynomial(self):
        expr = self.parsed_latex
        if expr.is_polynomial():
            return True
        else:
            return False
    def is_arithmeticExpr(self):
        expr = self.parsed_latex
        latex_expr = self.value
        # check if the expr can be evaluated to number
        if expr.is_number:
            # check if the expr invloves a definite integral or series
            if r'\sum' in latex_expr or r'\int' in latex_expr :
                return False
            else:
                return True
        else:
            return False
    def parse(self):
        self.parsed_latex = parse_latex(self.value)

    
        
    def method_not_found(self):
        pass
    def __str__(self)-> str:
        return str(self.value)
    def __repr__(self) -> str:
        return f'Expr({self.token})'