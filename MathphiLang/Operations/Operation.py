
from ..Core.Node import Node
from ..Core.TokenType import TokenType
from ..MathLiterals.MathLiteral import MathLiteral
# non-terminals
class Operation(Node):
    def __init__(self,op: TokenType,children: list):
        self.children = children
        self.op = op