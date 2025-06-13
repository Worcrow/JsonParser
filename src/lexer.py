from Tokenizer import *
import re


class lexer:
    def __init__(self):
        self.tokenStream = TokenStream()
    def add(self, type, char: str, lineNumber: int, columnNumber: int):
        token = Token(type, char.__repr__(), (lineNumber, columnNumber))
        self.tokenStream.add(token)
    def matchString(self, line: str, start: int, line_number: int) -> bool:
        if not line:
            return False
        matche = re.fullmatch(JsonTokenType.STRING.value, line)
        if matche:
            end = matche.end()
            token = Token(JsonTokenType.STRING, matche.group(), (line_number, start + 1))
            self.tokenStream.add(token)
            return (True)
        else:
            return (False)

    def matchNumber(self, line: str, start: int, line_number: int) -> bool:
        matches = re.search(JsonTokenType.NUMBER.value, line[start:])
        if matches:
            token = Token(JsonTokenType.NUMBER, matches.group(), (lineNumber, start + 1))
            self.tokenStream.add(token)
            return matches.end() + start
        return None

    def matchNull(self, line: str, start: int, lineNumber: int) -> bool:
        token = None
        if line and re.fullmatch(JsonTokenType.NULL.value, line):
            token = Token(JsonTokenType.NULL, line, (lineNumber, start + 1))
            self.tokenStream.add(token)
        return token != None

    def matchObject(self, line: str, start: int, lineNumber: int) -> bool:
        token = None
        if line and line[start] == '{':
            token = Token(JsonStructuredTypeSymbol.BEGINOBJECT, line[start], (lineNumber, start + 1))
            self.tokenStream.add(token)
        elif line and line[start] == '}':
            token = Token(JsonStructuredTypeSymbol.ENDOBJECT, line[start], (lineNumber, start + 1))
            self.tokenStream.add(token)
        return token != None

    def matchArray(self, line: str, start: int, lineNumber: int) -> bool:
        token = None
        if line and line[start] == '[':
            token = Token(JsonStructuredTypeSymbol.BEGINARRAY, line[start], (lineNumber, start + 1))
            self.tokenStream.add(token)
        
        elif line and line[start] == ']':
            token = Token(JsonStructuredTypeSymbol.ENDARRAY, line[start], (lineNumber, start + 1))
            self.tokenStream.add(token)
        return token != None

    def matchBoolean(self, line: str, start: int, lineNumber: int) -> bool:
        token = None
        if line and re.fullmatch(JsonTokenType.BOOLEAN.value, line):
            token = Token(JsonTokenType.BOOLEAN, line, (lineNumber, start + 1))
            self.tokenStream.add(token)
        return token != None

    def __repr__(self):
        tokensRep = []
        token = self.tokenStream.peek()
        while token is not None:
            tokensRep.append(token.__repr__())
            token = self.tokenStream.peek()
        return tokensRep[::-1]

def processLine(line: str, lineNumber: int, lexerObj):
    i = 0
    while i < len(line):
        pos = None
        if line[i] == '"':
            second_quote = re.search(r'"', line[i+1:])
            if second_quote:
                end = second_quote.start() + i + 1
                if not lexerObj.matchString(line[i:end + 1], i, lineNumber):
                    raise Exception(f'Error from if quote: Invalid String, line {lineNumber}, column {i + 1}')
                i = end
            else:
                raise Exception(f'Error from else quote: Invalid Token at line {lineNumber}, column {i + 1}')

        elif line[i] == ":":
            lexerObj.add(JsonStructuredTypeSymbol.NAMESEPARATOR, line[i], lineNumber, i + 1)
        elif line[i] == ",":
            lexerObj.add(JsonStructuredTypeSymbol.VALUESEPARATOR, line[i], lineNumber, i + 1)
        elif re.fullmatch(r'\s', line[i]):
            lexerObj.add(JsonStructuredTypeSymbol.WS, line[i], lineNumber, i + 1)
        elif lexerObj.matchBoolean(line[i: i + 4], i, lineNumber) or lexerObj.matchNull(line[i: i + 4], i, lineNumber):
            i += 3
        elif lexerObj.matchBoolean(line[i: i + 5], i, lineNumber):
            i += 4
        elif (pos := lexerObj.matchNumber(line, i, lineNumber)) != None:
            i += pos
        elif not (lexerObj.matchObject(line, i, lineNumber) or lexerObj.matchArray(line, i, lineNumber)):
            raise Exception(f'Error from elif not: Invalid Token at line {lineNumber}, column {i + 1}') 
        i += 1

with open("/Users/oel-asri/Kingsave/json-parser/unit_test/validJson1.json", 'r') as validJson:
    lineNumber = 0
    lex = lexer()
    lines = validJson.readlines()
    for line in lines:
        lineNumber += 1
        processLine(line, lineNumber, lex)

    print(*lex.__repr__())

