from .Operation import Operation
from ..Core.TokenType import TokenType
from ..MathLiterals.MathLiteral import MathLiteral

class Factorize(Operation):
    def __init__(self,children: list):
        super().__init__(op =TokenType.FACTORIZE, children = children)
        self.child = children[0]

    