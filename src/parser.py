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
        while self.current() != "EOF" and self.current().type == JsonStructuredTypeSymbol.WS:
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
        self.skipSpace()

        while self.current() != "EOF":
            token = self.current()
            if token.type == JsonStructuredTypeSymbol.BEGINOBJECT:
                root.value = self.advance(JsonStructuredTypeSymbol.BEGINOBJECT)
                if self.current().type == JsonStructuredTypeSymbol.ENDOBJECT:
                    self.advance(JsonStructuredTypeSymbol.ENDOBJECT)
                    return root
                return self.parseObject(root)

            elif token.type in self.values:
                return primitiveTypeNode(self.advance(token.type))

            elif token.type == JsonStructuredTypeSymbol.ENDOBJECT:
                raise Exception("Expected value")

    def parseObject(self, root):
        if self.current() == "EOF":
            raise Exception("Encountre EOF, Instead A Key")
        node = pairNode(None, None)
        node.key = self.advance(JsonTokenType.STRING)
        self.advance(JsonStructuredTypeSymbol.NAMESEPARATOR)
        node.value = self.parse()
        root.appendChild(node)
        if self.current().type == JsonStructuredTypeSymbol.ENDOBJECT:       
            self.advance(JsonStructuredTypeSymbol.ENDOBJECT)
            return root
        self.advance(JsonStructuredTypeSymbol.VALUESEPARATOR)
        return self.parseObject(root)


lex = processFile("/Users/oel-asri/Kingsave/JsonParser/unit_test/validJson1.json")
# print(lex.tokenStream.Token)

parser = Parser(lex.tokenStream.Token)
ast = parser.parse()

print(ast)
