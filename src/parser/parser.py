from src.parser.lexer import *
import sys

sys.path.extend(['/Users/mac/JsonParser/error'])
from error_handler import JsonParserError


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
        eof = Token(JsonTokenType.EOF, 'EOF', (self.tokens[-1].position[0] + 1, self.tokens[-1].position[1]))
        self.tokens.append(eof)
        self.inStructuredType = 0

    def current(self):
        return self.tokens[self.ind]

    def is_eof(self):
        return self.current().type == JsonTokenType.EOF

    def skipSpace(self):
        while self.current().type == JsonStructuredTypeSymbol.WS:
            self.ind += 1

    def advance(self, expectedTokenType):
        token = self.current()
        if token.type == expectedTokenType:
            self.ind += 1
            self.skipSpace()
            return token
        raise JsonParserError(
            f"Syntax Error at line {token.position[0]}, column {token.position[1]}: "
            f"Expected token type `{expectedTokenType}`, but got `{token.type}` with value `{token.value!r}`"
        )        

    def parse(self):
        self.skipSpace()
        current_token = self.current()
        top_level = ''
        root = AST(current_token)
        if self.is_eof():
            return

        if current_token.type == JsonStructuredTypeSymbol.BEGINOBJECT:
            root = self.parse_object(root)
            top_level = 'object'

        elif current_token.type == JsonStructuredTypeSymbol.BEGINARRAY:
            root = self.parse_array(root)
            top_level = 'array'

        elif current_token.type in self.primitives:
            self.advance(current_token.type)
            root.value = primitiveTypeNode(current_token)
            top_level = 'primitive'

        if not self.is_eof():
            raise JsonParserError(
                f'Expected end of input after top-level {top_level}, but found `{self.current().type}'
                f' with value {self.current().value!r}', self.current().position
            )

        return root

    def parse_value(self):
        current_token = self.current()

        if self.is_eof():
            raise JsonParserError(
                "Syntax Error: Expected a JSON value (object, array, string, number, boolean, or null), but reached end of input"
            )

        if current_token.type in self.primitives:
            self.advance(current_token.type)
            return primitiveTypeNode(current_token)
    
        if current_token.type == JsonStructuredTypeSymbol.BEGINOBJECT:
            root = AST(current_token)
            return self.parse_object(root)

        if current_token.type == JsonStructuredTypeSymbol.BEGINARRAY:
            root = AST(current_token)
            return self.parse_array(root)

        raise JsonParserError(
            f"Syntax Error at line {current_token.position[0]}, column {current_token.position[1]}: "
            f"Unexpected token `{current_token.type}` with value {current_token.value!r}. "
            f"Expected a JSON value (object, array, string, number, boolean, or null).",
            current_token.position
        )
    
    def parse_object(self, root):
        current_token = self.current()

        if current_token.type == JsonStructuredTypeSymbol.BEGINOBJECT:
            root.value = current_token
            self.advance(JsonStructuredTypeSymbol.BEGINOBJECT)
            if self.is_eof():
                raise JsonParserError(
                    "Syntax Error: Object not properly closed. Expected `}` before end of file.",
                    self.current().position
                )
            if self.current().type == JsonStructuredTypeSymbol.ENDOBJECT:
                self.advance(JsonStructuredTypeSymbol.ENDOBJECT)
                return root

        key = self.advance(JsonTokenType.STRING)
        self.advance(JsonStructuredTypeSymbol.NAMESEPARATOR)
        value = self.parse_value()
        node = pairNode(key, value)
        root.appendChild(node)

        if self.is_eof():
            raise JsonParserError(
                "Syntax Error: Object not properly closed. Expected `}` before end of file.",
                self.current().position
            )

        current_token = self.current()
        if current_token.type != JsonStructuredTypeSymbol.ENDOBJECT:
            self.advance(JsonStructuredTypeSymbol.VALUESEPARATOR)
            return self.parse_object(root)

        if current_token.type == JsonStructuredTypeSymbol.ENDOBJECT:
            self.advance(JsonStructuredTypeSymbol.ENDOBJECT)
            return root
        
        raise JsonParserError(
            f"Syntax Error: Unexpected token `{current_token.type}` with value {current_token.value!r}. "
            f"Expected `,` or `{'}'}` in object.",
            current_token.position
        )

    def parse_array(self, root):
        root.value = self.advance(JsonStructuredTypeSymbol.BEGINARRAY)

        if self.is_eof():
            raise JsonParserError(
                "Unexpected end of input: Expected elements or ']' to close the array.",
                self.current().position
            )
        
        if self.current().type == JsonStructuredTypeSymbol.ENDARRAY:
            self.advance(JsonStructuredTypeSymbol.ENDARRAY)
            return root

        while True:
            element = self.parse_value()
            root.appendChild(element)
            current_token = self.current()

            if self.is_eof():
                raise JsonParserError(
                    "Unexpected end of input: Expected ',' or ']' after array element.",
                    self.current().position
                )

            elif current_token.type == JsonStructuredTypeSymbol.ENDARRAY:
                self.advance(JsonStructuredTypeSymbol.ENDARRAY)
                break
            elif current_token.type == JsonStructuredTypeSymbol.VALUESEPARATOR:
                self.advance(JsonStructuredTypeSymbol.VALUESEPARATOR)
                if self.is_eof():
                    raise JsonParserError(
                        "Syntax Error: Expected JSON value after `,`, but encountered EOF.",
                        self.current().position
                    )
                elif self.current().type == JsonStructuredTypeSymbol.ENDARRAY:
                    raise JsonParserError(
                        "Syntax Error: Trailing comma before `]` is not allowed in JSON arrays.",
                        self.current().position
                    )

        return root


# lex = processFile("../unit_test/MOCK_DATA.json")

# # print(lex.tokenStream.Token)

# parser = Parser(lex.tokenStream.Token)
# ast = parser.parse()

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

# print_ast_json(ast)
