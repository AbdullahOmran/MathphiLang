
from MathphiLang.Core.Node import Node
from MathphiLang.Core.TokenType import TokenType
from MathphiLang.MathLiterals.Integer import Integer
from MathphiLang.MathLiterals.Expr import Expr
from MathphiLang.Core.Lexer import Lexer
from MathphiLang.Operations.Factorize import Factorize
from MathphiLang.Operations.Expand import Expand



class Parser(object):
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('invalid syntax')
    
    def eat(self, token_type: TokenType):
        if self.current_token.token_type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    #
    # Parser grammar is written here
    #
    # syntax rule 
    # statement: operation
    # params: (INTEGER | EXPR)*
    # operation: (FACTORIZE | EXPAND) params
    #  
    def statement (self):
       return self.operation()
      
            
    def params(self):
         literals = []
         while self.current_token.token_type in (TokenType.INTEGER , TokenType.EXPR):
           token = self.current_token
           if token.token_type == TokenType.INTEGER:
               self.eat(TokenType.INTEGER)
               literals.append(Integer(token))
           elif token.token_type == TokenType.EXPR:
               self.eat(TokenType.EXPR)
               literals.append(Expr(token))
         return literals
    
    def operation (self):
        token = self.current_token
       
        if token.token_type == TokenType.FACTORIZE:
            self.eat(TokenType.FACTORIZE)
            literals= self.params()
            return Factorize(literals)
        elif token.token_type == TokenType.EXPAND:
            self.eat(TokenType.EXPAND)
            literals= self.params()
            return Expand(literals)
        
    
        

    def parse(self):
        return self.statement()
