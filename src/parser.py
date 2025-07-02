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
        self.values = (JsonTokenType.STRING, JsonTokenType.NUMBER, JsonTokenType.NULL,\
                       JsonTokenType.BOOLEAN)

    def current(self):
        return self.tokens[self.ind]

    def skipSpace(self):
        while self.current().type == JsonStructuredTypeSymbol.WS:
            self.ind += 1

    def advance(self, expectedTokenType):
        token = self.current()
        if token.type == expectedTokenType:
            self.ind += 1
            self.skipSpace()
            return token
        print(token.__repr__())
        raise Exception(f"Invalid syntax line: {token.position[0]} column: {token.position[1]}\nExepected: {expectedTokenType}, Got: {token.type}")

    def parse(self):
        root = AST(None, None, None)
        self.parseValue(root)
        return root

    def parseValue(self, root):
        token = self.current()
        if token.type == JsonStructuredTypeSymbol.BEGINOBJECT:
            self.advance(JsonStructuredTypeSymbol.BEGINOBJECT)
            if self.current().type == JsonStructuredTypeSymbol.ENDOBJECT:
                return AST(Token(JsonTokenType.EMPTYOBJECT, '', token.position))
            root = AST(token, None, None)
            left = AST(self.advance(JsonTokenType.STRING), None, None)
            self.advance(JsonStructuredTypeSymbol.NAMESEPARATOR)
            right = self.parseValue()
            root.left = left
            root.right = right
            if self.current().type == JsonStructuredTypeSymbol.ENDOBJECT:
                return root
            self.advance(JsonStructuredTypeSymbol.VALUESEPARATOR)
            return root

        elif token.type in self.values:
            self.ind += 1
            self.skipSpace()
            return AST(token, None, None)

        else:
            raise Exception(f"Invalid Syntax line: {token.position[0]} column: {token.position[1]}")
        
        
        

lex = processFile("/Users/mac/JsonParser/unit_test/validJson1.json")

parser = Parser(lex.tokenStream.Token)
ast = parser.parse()

print(ast.right.right)