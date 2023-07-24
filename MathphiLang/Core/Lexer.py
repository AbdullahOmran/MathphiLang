from .Token import Token
from .TokenType import TokenType

class Lexer(object):
    def __init__(self,text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
    def error(self):
        raise Exception('invalid word')
    
    def advance(self):
        # move the pos a forward step
        # update the current character of the lexer
        self.pos += 1
        if self.pos > len(self.text)-1 :
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        # ignore the space between words
        while (self.current_char is not None) and (self.current_char.isspace()):
            self.advance()

    def get_next_token(self):
        # this method responsible for breaking the text into tokens 
        # one token at a time
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
               integer_value =  self.integer()
               token = Token(token_type = TokenType.INTEGER , value = integer_value)
               token.length = len(str(integer_value))
               token.start = self.pos - token.length
               return token
            # get latex expression
            if self.current_char =='$':
                latex = self.latex()
                token = Token(token_type = TokenType.EXPR, value = latex)
                
                token.length = len(str(latex))+4
                token.start = self.pos - token.length
                return token
            if self.current_char.isalpha():
                word = self.word()
                
                if (word == TokenType.FACTORIZE.value):
                    token =  Token(token_type = TokenType.FACTORIZE, value = word)
                    
                    token.length = len(str(word))
                    token.start = self.pos - token.length
                    return token
                if (word == TokenType.EXPAND.value):
                    token =  Token(token_type = TokenType.EXPAND, value = word)
                    token.length = len(str(word))
                    token.start = self.pos - token.length
                    return token
            self.error()
        token = Token(token_type = TokenType.EOF,value = None)
        token.length = len(str(self.text))
        token.start = self.pos - token.length
        return token
            
    def integer(self):
        integer_value = ''
        while (self.current_char is not None) and self.current_char.isdigit():
            integer_value += self.current_char
            self.advance()
        return int(integer_value)
    def word(self):
        word  = ''
        while (self.current_char is not None) and self.current_char.isalpha():
            word += self.current_char
            self.advance()
        return str(word)
    def latex(self):
        latex  = ''
        if self.current_char == '$':
            self.advance()
            if self.current_char == '$':
               self.advance()
               while (self.current_char is not None) and( (self.current_char.isalpha())  \
                  or (self.current_char in ('\\[]{}.'))or (self.current_char.isdigit())) :
                  latex += self.current_char
                  
                  self.advance()
               if self.current_char == None:
                   self.error()
               if self.current_char =='$':
                   self.advance()
                   if self.current_char =='$':
                      self.advance()
                       
                   else:
                       self.error()
               else:
                   self.error()
            else:
                self.error()
        else:
            self.error()
        return latex
              