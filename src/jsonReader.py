from src.parser import lexer, parser
from src.evaluator.evaluator import Converter


def jsonReader(file_path: str):
    lex = lexer.processFile(file_path)
    Parser = parser.Parser(lex.tokenStream.Token)
    ast = Parser.parse()
    evaluator = Converter()
    json = evaluator.convert(ast)
    return json