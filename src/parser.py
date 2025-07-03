from lexer import *

class pairNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class primitiveTypeNode:
    def __init__(self, value):
        self.value = value

class AST:
    def __init__ (self, token):
        self.value = token
        self.child = []

    def appendChild(self, child):
        self.child.append(child)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.ind = 0
        self.values = (JsonTokenType.STRING, JsonTokenType.NUMBER, JsonTokenType.NULL,\
                       JsonTokenType.BOOLEAN)
        self.tokens.append("EOF")

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

        raise Exception(f"Invalid syntax line: {token.position[0]} column: {token.position[1]}\nExepected: {expectedTokenType}, Got: {token.type}")

    def parse(self):
        root = AST(None)
        while self.current() != "EOF":
            token = self.current()
            if token.type == JsonStructuredTypeSymbol.BEGINOBJECT:
                root.value = self.advance(JsonStructuredTypeSymbol.BEGINOBJECT)
                self.parseObject(root)
            elif token.type in self.values:
                return primitiveTypeNode(self.advance(token.type))

    def parseObject(self, root):
        while self.current().type != JsonStructuredTypeSymbol.ENDOBJECT:
            node = pairNode(None, None)
            node.key = self.advance(JsonTokenType.STRING)
            self.advance(JsonStructuredTypeSymbol.NAMESEPARATOR)
            node.value = self.parse()
            root.appendChild(node)
            if self.current().type == JsonStructuredTypeSymbol.ENDOBJECT:
                self.advance(JsonStructuredTypeSymbol.ENDOBJECT)
                return root
            self.advance(JsonStructuredTypeSymbol.VALUESEPARATOR)


lex = processFile("/Users/mac/JsonParser/unit_test/validJson1.json")

parser = Parser(lex.tokenStream.Token)
ast = parser.parse()

print(ast.right.right)