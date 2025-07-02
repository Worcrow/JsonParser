from lexer import *

class AST:
    def __init__ (self, token, left, right):
        self.node = token
        self.left = left
        self.right = right

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.ind = 0

    def current(self):
        return self.tokens[self.ind]

    def skipSpace(self):
        while self.current().type == JsonStructuredTypeSymbol.WS:
            self.ind += 1

    def advance(self, expectedTokenType):
        token = self.current()
        if token.type == expectedTokenType:
            self.ind += 1
            return token

        raise Exception(f"Invalid syntax line: {token.position[0]} column: {token.position[1]}\nExepected: {expectedTokenType}, Got: {token.type}")

    def parse(self):
       return self.parseValue()

    def parseValue(self):
        token = self.current()
        if token.type == JsonStructuredTypeSymbol.BEGINOBJECT:
            self.advance(JsonStructuredTypeSymbol.BEGINOBJECT)
            self.skipSpace()
            if self.current().type == JsonStructuredTypeSymbol.ENDOBJECT:
                return AST(Token(JsonTokenType.EMPTYOBJECT, '', token.position))
            root = AST(token, None, None)
            left = AST(self.advance(JsonTokenType.STRING), None, None)
            self.advance(JsonStructuredTypeSymbol.NAMESEPARATOR)
            right = self.parseValue()
            self.advance(JsonStructuredTypeSymbol.VALUESEPARATOR)
            root.left = left
            root.right = right

            return root


lex = processFile("/Users/oel-asri/Kingsave/JsonParser/unit_test/validJson1.json")

parser = Parser(lex.tokenStream.Token)
parser.parse()

print(parser.root.node)