from lexer import *
import sys

sys.setrecursionlimit(3000)

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
        self.primitives = (JsonTokenType.STRING, JsonTokenType.NUMBER, JsonTokenType.NULL,\
                       JsonTokenType.BOOLEAN)
        self.tokens.append("EOF")
        self.inStructuredType = 0

    def current(self):
        # self.skipSpace()
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
        self.skipSpace()
        current_token = self.current()
        root = AST(None)
        if current_token == "EOF":
            return
        if current_token.type == JsonStructuredTypeSymbol.BEGINOBJECT:
            root = self.parse_object(root)
            if self.current() != "EOF":
                raise Exception(f"Expected EOF, encouter {self.current().value}")
        return root

    def parse_value(self):
        current_token = self.current()

        if current_token.type in self.primitives:
            self.advance(current_token.type)
            return primitiveTypeNode(current_token)
    
        if current_token.type == JsonStructuredTypeSymbol.BEGINOBJECT:
            root = AST(current_token)
            self.parse_object(root)
            return root

        if current_token.type == JsonStructuredTypeSymbol.BEGINARRAY:
            root = AST(current_token)
            self.parse_array(root)
            return root

    
    def parse_object(self, root):
        current_token = self.current()

        if current_token != 'EOF' and current_token.type == JsonStructuredTypeSymbol.BEGINOBJECT:
            root.value = current_token
            self.advance(JsonStructuredTypeSymbol.BEGINOBJECT)
            token = self.current()
            if token != 'EOF' and token.type == JsonStructuredTypeSymbol.ENDOBJECT:
                self.advance(JsonStructuredTypeSymbol.ENDOBJECT)
                return root

        key = self.advance(JsonTokenType.STRING)
        self.advance(JsonStructuredTypeSymbol.NAMESEPARATOR)
        value = self.parse_value()
        node = pairNode(key, value)
        root.appendChild(node)

        current_token = self.current()
        if current_token == "EOF":
            raise Exception("Error: Encounter EOF")
        if current_token.type != JsonStructuredTypeSymbol.ENDOBJECT:
            self.advance(JsonStructuredTypeSymbol.VALUESEPARATOR)
            self.parse_object(root)

        if current_token != 'EOF' and current_token.type != JsonStructuredTypeSymbol.ENDOBJECT:
            raise Exception(f"Invalid Syntax Line: {current_token.position[0]} Column: {current_token.position[1]}")
        
        self.advance(JsonStructuredTypeSymbol.ENDOBJECT)
        return root
        
    def parse_array(self, root):
        pass



lex = processFile("/Users/oel-asri/Kingsave/JsonParser/unit_test/test.json")

# print(lex.tokenStream.Token)

parser = Parser(lex.tokenStream.Token)
ast = parser.parse()


print_ast_json(ast)

# print(ast.value)
