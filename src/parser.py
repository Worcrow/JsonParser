from lexer import *

class AST:
    def __init__ (self, token, left, right):
        self.node = token
        self.left = left
        self.right = right

class Parser:
    def __init__(self, lex):
        self.lexer = lex
        self.root = None
        self.currentToken = 0
        self.trackOA = []
        self.value = (JsonTokenType.STRING, JsonTokenType.NUMBER, JsonTokenType.BOOLEAN, JsonTokenType.NULL)
    
    def isTerm(self, index):
        for ind in range(index, len(self.lexer)):
            if self.lexer[ind].type != JsonStructuredTypeSymbol.WS:
                print(self.lexer[ind].type)
                return False
        return True

    def parse(self):
        while self.currentToken < len(self.lexer):
            if self.lexer[self.currentToken].type == JsonStructuredTypeSymbol.WS:
                self.currentToken += 1
                continue
            if self.lexer[self.currentToken].type == JsonStructuredTypeSymbol.BEGINOBJECT:
                pass
            elif self.lexer[self.currentToken].type == JsonStructuredTypeSymbol.BEGINARRAY:
                pass
            elif self.lexer[self.currentToken].type in self.value and self.isTerm(self.currentToken + 1):
                self.root = AST(self.lexer[self.currentToken], None, None)
            
            else:
                line, column = self.lexer[self.currentToken].position
                raise Exception(f"Error: Invalid Syntax at {line} {column}")
            self.currentToken += 1


lex = processFile("/Users/oel-asri/Kingsave/JsonParser/unit_test/validJson1.json")

parser = Parser(lex.tokenStream.Token)
parser.parse()

print(parser.root.node)