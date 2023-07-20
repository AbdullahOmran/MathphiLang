
from MathphiLang.Core.Node import Node
from MathphiLang.Core.TokenType import TokenType
from MathphiLang.MathLiterals.MathLiteral import MathLiteral
# non-terminals
class Operation(Node):
    def __init__(self,op: TokenType,children: list):
        self.children = children
        self.op = op