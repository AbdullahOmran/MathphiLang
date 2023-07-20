from MathphiLang.MathLiterals.MathLiteral import MathLiteral
from MathphiLang.Core.Token import Token

class Expr(MathLiteral):
    def __init__(self,token: Token):
        self.token = token
        self.value = token.value
