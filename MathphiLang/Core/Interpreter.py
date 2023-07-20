from MathphiLang.Core.NodeVisitor import NodeVisitor
from MathphiLang.Core.TokenType import TokenType
from MathphiLang.Core.Parser import Parser
from MathphiLang.Core.Node import Node


class Interpreter(NodeVisitor):
    def __init__(self,parser: Parser):
        self.parser = parser
        
    def visit_op(self,node: Node):
        if node.op.token_type == TokenType.INTEGER:
            return self.visit(node.left)
    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)