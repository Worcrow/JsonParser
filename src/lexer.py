import re
import os
from src.Tokenizer import *

class lexer:
    def __init__(self):
        self.tokenStream = TokenStream()
    def add(self, type, char: str, lineNumber: int, columnNumber: int):
        token = Token(type, char, (lineNumber, columnNumber))
        self.tokenStream.add(token)
    def matchString(self, line: str, start: int, lineNumber: int) -> bool:
        if not line:
            return False
        matche = re.fullmatch(JsonTokenType.STRING.value, line)
        if matche:
            token = Token(JsonTokenType.STRING, matche.group(), (lineNumber, start + 1))
            self.tokenStream.add(token)
            return (True)
        else:
            return (False)

    def matchNumber(self, line: str, start: int, lineNumber: int) -> bool:
        matches = re.fullmatch(JsonTokenType.NUMBER.value, line)
        if matches:
            token = Token(JsonTokenType.NUMBER, matches.group(), (lineNumber, start + 1))
            self.tokenStream.add(token)
            return True
        return False

    def matchNull(self, line: str, start: int, lineNumber: int) -> bool:
        token = None
        if line and re.fullmatch(JsonTokenType.NULL.value, line):
            token = Token(JsonTokenType.NULL, line, (lineNumber, start + 1))
            self.tokenStream.add(token)
        return token != None
    
    def matchBoolean(self, line: str, start: int, lineNumber: int) -> bool:
        token = None

        if line and re.fullmatch(JsonTokenType.BOOLEAN.value, line):
            token = Token(JsonTokenType.BOOLEAN, line, (lineNumber, start + 1))
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
    

    def __repr__(self):
        tokensRep = []
        token = self.tokenStream.peek()
        while token is not None:
            tokensRep.append(token.__repr__())
            token = self.tokenStream.peek()
        return tokensRep[::-1]

def tokenize_string(line, start, lineNumber, lexerObj):
    second_quote = re.search(r'(?<!\\)"', line[start + 1:])
    if not second_quote:
        raise Exception(f'Error: Invalid String, line {lineNumber}, column {start + 1}')
    end = second_quote.start() + start + 1
    if not lexerObj.matchString(line[start:end + 1], start, lineNumber):
        raise Exception(f'Error : Invalid String, line {lineNumber}, column {start + 1}')
    return end

def tokenize_digit(line, start, lineNumber, lexerObj):
    end = start
    while end < len(line) and line[end] not in "\t\r\n,]}\f\v ":
        end += 1
    if lexerObj.matchNumber(line[start:end], start, lineNumber):
        return end - 1
    else:
        raise Exception(f"Error : Invalid Number, line {lineNumber}, column {start + 1}")

def processLine(line: str, lineNumber: int, lexerObj):
    i = 0
    while i < len(line):
        if line[i] == '"':
            i = tokenize_string(line, i, lineNumber, lexerObj)
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
        elif line[i].isdigit() or line[i] == "-":
            i = tokenize_digit(line, i, lineNumber, lexerObj)    
        elif line[i] == '{' or line[i] == '}':
            lexerObj.matchObject(line, i, lineNumber)
        elif line[i] == ']' or line[i] == '[':
            lexerObj.matchArray(line, i, lineNumber)
        else:
            raise Exception(f'Error : Invalid Token at line {lineNumber}, column {i + 1}') 
        i += 1

def processFile(path:str):
    lex = lexer()
    with open(path, 'r') as jsonFile:
        lineNumber = 0
        lines = jsonFile.readlines()
        for line in lines:
            lineNumber += 1
            processLine(line, lineNumber, lex)
    return (lex)

