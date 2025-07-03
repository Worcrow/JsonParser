from lexer import *
import sys

sys.setrecursionlimit(3000)

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
        self.inStructuredType = 0

    def current(self):
        return self.tokens[self.ind]

    def skipSpace(self):
        while self.current() != "EOF" and self.current().type == JsonStructuredTypeSymbol.WS:
            self.ind += 1

    def advance(self, expectedTokenType):
        token = self.current()
        if token != "EOF" and token.type == expectedTokenType:
            self.ind += 1
            self.skipSpace()
            return token

        raise Exception(f"Invalid syntax line: {token.position[0]} column: {token.position[1]}\nExepected: {expectedTokenType}, Got: {token.type}")

    def parse(self):
        root = AST(None)
        self.skipSpace()

        while self.current() != "EOF":
            token = self.current()
            if token != "EOF" and token.type == JsonStructuredTypeSymbol.BEGINOBJECT:
                root.value = self.advance(JsonStructuredTypeSymbol.BEGINOBJECT)
                self.inStructuredType += 1
                if self.current() == "EOF":
                    raise Exception("Expected end of Object, Got: EOF")
                if self.current().type == JsonStructuredTypeSymbol.ENDOBJECT:
                    self.advance(JsonStructuredTypeSymbol.ENDOBJECT)
                    self.inStructuredType -= 1
                    return root
                return self.parseObject(root)

            elif token != "EOF" and token.type == JsonStructuredTypeSymbol.BEGINARRAY:
                root.value = self.advance(JsonStructuredTypeSymbol.BEGINARRAY)
                self.inStructuredType += 1
                if self.current() == "EOF":
                    raise Exception("Expected end of array, Got: EOF")
                if self.current().type == JsonStructuredTypeSymbol.ENDARRAY:
                    self.advance(JsonStructuredTypeSymbol.ENDARRAY)
                    self.inStructuredType -= 1
                    return root
                return self.parseArray(root)

            elif token != "EOF" and self.inStructuredType > 0 and token.type in self.values:
                return primitiveTypeNode(self.advance(token.type))

            elif token != "EOF" and self.inStructuredType <= 0 and token.type in self.values:
                root.key = self.termToken(token)
                return root

            # elif token != "EOF" and token.type == JsonStructuredTypeSymbol.ENDOBJECT:
            #     raise Exception("Expected value")
            # elif token != "EOF" and token.type == JsonStructuredTypeSymbol.ENDARRAY:
            #     raise Exception("Expected value array")
            elif token != "EOF" :
                raise Exception("Encouter EOF")

    def parseObject(self, root):
        if self.current() == "EOF":
            raise Exception("Encountre EOF, Instead A Key")
        node = pairNode(None, None)
        node.key = self.advance(JsonTokenType.STRING)
        self.advance(JsonStructuredTypeSymbol.NAMESEPARATOR)
        node.value = self.parse()
        root.appendChild(node)
        if self.current() != "EOF" and self.current().type == JsonStructuredTypeSymbol.ENDOBJECT:       
            self.advance(JsonStructuredTypeSymbol.ENDOBJECT)
            self.inStructuredType -= 1
            return root
        self.advance(JsonStructuredTypeSymbol.VALUESEPARATOR)
        return self.parseObject(root)

    def parseArray(self, root):
        root.appendChild(self.parse())
        if self.current() != "EOF" and self.current().type == JsonStructuredTypeSymbol.ENDARRAY:
            self.advance(JsonStructuredTypeSymbol.ENDARRAY)
            self.inStructuredType -= 1
            return root
        self.advance(JsonStructuredTypeSymbol.VALUESEPARATOR)
        return self.parseArray(root)

    def termToken(self, token):
        self.advance(token.type)
        self.skipSpace()
        current = self.current()
        if (current != "EOF"):
            raise Exception(f"Invalid Syntax line: {current.position[0]} column: {current.position[1]}")
        return token

lex = processFile("/Users/oel-asri/Kingsave/JsonParser/unit_test/MOCK_DATA.json")

# print(lex.tokenStream.Token)

parser = Parser(lex.tokenStream.Token)
ast = parser.parse()


def print_ast_json(node, indent=0, is_last=True, is_key=False):
    indent_str = "    " * indent
    connector = "└── " if is_last else "├── "

    if isinstance(node, AST):
        print(f"{indent_str}{connector}AST({node.value})")
        for i, child in enumerate(node.child):
            print_ast_json(child, indent + 1, i == len(node.child) - 1)
    elif isinstance(node, pairNode):
        print(f"{indent_str}{connector}pairNode:")
        print(f"{indent_str}    ├── key: {node.key}")
        print(f"{indent_str}    └── value:")
        print_ast_json(node.value, indent + 2, True, True)
    elif isinstance(node, primitiveTypeNode):
        print(f"{indent_str}{connector}primitiveTypeNode: {node.value}")
    else:
        print(f"{indent_str}{connector}Unknown node type: {type(node)}")


print_ast_json(ast)
