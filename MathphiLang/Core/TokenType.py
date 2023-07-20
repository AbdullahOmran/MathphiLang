from enum import Enum

class TokenType(Enum):
    INTEGER = 'INTEGER'
    EOF = 'EOF'
    EXPR = 'EXPR'
    FACTORIZE = 'factorize'
    EXPAND = 'expand'