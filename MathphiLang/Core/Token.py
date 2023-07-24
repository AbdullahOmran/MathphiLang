from .TokenType import TokenType

class Token(object):
    def __init__(self,token_type: TokenType, value):
        self.token_type = token_type
        self.value =value
        self.length = 0
        self.start = 0
        
    def __str__(self):
        return f'Token({self.token_type},{self.value},{self.start},{self.length})'
    def __repr__(self):
        return self.__str__()
    