from MathphiLang.MathLiterals.MathLiteral import MathLiteral
from MathphiLang.Core.Token import Token

class Integer(MathLiteral):
    def __init__(self, token: Token):
        self.token = token
        self.value = self.token.value
