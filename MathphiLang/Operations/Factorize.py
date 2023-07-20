from MathphiLang.Operations.Operation import Operation
from MathphiLang.Core.TokenType import TokenType
from MathphiLang.MathLiterals.MathLiteral import MathLiteral

class Factorize(Operation):
    def __init__(self,children):
        super().__init__(op =TokenType.FACTORIZE, children = children)
        self.child = children[0]

    