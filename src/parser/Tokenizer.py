from enum import Enum

class JsonStringSymbol(Enum):
    CHAR = r'[^"\\]'
    ESCAPECHAR = r'["\\/bnrft]'
    ESCAPED = r'\\' + ESCAPECHAR
    QUOTATIONMARK = r'"'

class JsonNumberSymbol(Enum):
    DIGITS = r'[0-9]'
    DIGITS19 = r'[1-9]'
    DECIMALPOINT = r'\.'
    EX = r'[Ee]'
    MINUS = r'-'
    PLUS = r'+'
    INT = r'(?:0(?!' + DIGITS + r')|' + DIGITS19 + DIGITS + r'*)'
    EXP = EX + r'[' + PLUS + MINUS + r']?' + DIGITS + r'+'
    FRACT = DECIMALPOINT + DIGITS + r'+' 

class JsonStructuredTypeSymbol(Enum):
    WS = r'\s'
    BEGINARRAY = r'\['
    ENDARRAY = r'\]'
    BEGINOBJECT = r'\{'
    ENDOBJECT = r'\}'
    NAMESEPARATOR = r':'
    VALUESEPARATOR = r','


class JsonTokenType(Enum):
    STRING = JsonStringSymbol.QUOTATIONMARK.value + r'(?:' +\
                JsonStringSymbol.ESCAPED.value + r'|' + JsonStringSymbol.CHAR.value + \
             r')*' + JsonStringSymbol.QUOTATIONMARK.value 
    NUMBER = r'(' + \
                JsonNumberSymbol.MINUS.value + r'?' + \
                JsonNumberSymbol.INT.value +\
                r'(?:' + JsonNumberSymbol.FRACT.value + r')?' + \
                r'(?:' + JsonNumberSymbol.EXP.value + r')?' + \
            r')'
    BOOLEAN = r'(true|false)'
    NULL = r'(null)'
    EMPTYOBJECT = r''
    EMPTYARRAY = r''
    EOF = r'EOF'


class Token:
    def __init__(self, type, value, position): #position like (line, column)
        self.type = type
        self.value = value
        self.position = position
    def __repr__(self):
        return f'Token(type: {self.type}, value: {self.value.__repr__()}, position: {list(self.position)})'

class TokenStream:
    def __init__(self):
        self.Token = []
        self.position = 0
    def add(self, token):
        self.Token.append(token)
        self.position += 1
    def peek(self):
        token = None
        if self.position > 0:
            token = self.Token[self.position - 1]
            self.position -= 1
        return token
        