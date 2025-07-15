# 📦 JSON Parser in Python (AST-Based)

This project is a hand-written **recursive descent parser** that reads and parses JSON files **without using Python’s built-in `json` module`**. It builds an **Abstract Syntax Tree (AST)** and then converts it into native Python data types:  
`dict`, `list`, `str`, `int`, `float`, `bool`, and `None`.

---

## 🧠 Why This Exists

This parser was built to deeply understand:

- ✅ How real parsers work under the hood
- ✅ Tokenization (lexing) and grammar-based parsing
- ✅ AST construction and recursive tree traversal
- ✅ Manual error reporting using token line/column positions
- ✅ JSON grammar and formal structure (RFC-7159)

---

## 🚀 Features

- 🔁 Fully recursive descent parser (no parser generator)
- 🧪 Lexer/tokenizer with token stream and position tracking
- 🌲 Custom AST nodes:
  - `AST` — structured types (`{}` or `[]`)
  - `pairNode` — key/value pairs inside objects
  - `primitiveTypeNode` — terminal values (string, number, etc.)
- ❗ Error handling with accurate position via `JsonParserError`
- 🔍 Compatible with strict JSON (RFC-7159)
- 🔄 Manual AST-to-Python evaluation logic

---

## 🧩 Project Structure

- **src/**
  - `parser.py` — main recursive descent parser
  - `lexer.py` — generates the token stream from JSON text
  - `tokenizer.py` — defines token types, positions, and token stream
  - `__init__.py` — marks `src/` as a Python package

- **error/**
  - `error_handler.py` — defines custom exception classes (e.g. `JsonParserError`)
  - `__init__.py` — marks `error/` as a Python package

- **unit_test/**
  - `validJson1.json`, `validJson2.json`, ... — sample test files
  - `MOCK_DATA.json` — a large dataset to stress test the parser

- **README.md** — documentation for the project

---

## 🧪 Sample Output

Parsing this JSON:

```json
{
  "name": "John",
  "age": 30,
  "hobbies": ["reading", "gaming"]
}
```

└── AST(Token('{'))
    ├── pairNode:
    │   ├── key: "name"
    │   └── value:
    │       └── primitiveTypeNode: "John"
    ├── pairNode:
    │   ├── key: "age"
    │   └── value:
    │       └── primitiveTypeNode: 30
    ├── pairNode:
    │   ├── key: "hobbies"
    │   └── value:
    │       └── AST(Token('['))
    │           ├── primitiveTypeNode: "reading"
    │           └── primitiveTypeNode: "gaming"

---

## 📚 Learnings

Through building this parser from scratch, the following core concepts were explored:

- 🔍 Recursive descent parsing strategies
- ✂️ Tokenization and whitespace handling
- 🌳 AST data modeling and structure
- 🧠 JSON grammar (objects, arrays, values)
- ⚙️ Clean project/module structuring with `__init__.py`
- 🛠️ Error handling with token context (line/column)

---

## 📥 Future Improvements

- ✅ AST → Python conversion utility (like `json.loads`)
- ✅ Semantic validation (duplicate keys, strict types)
- ✅ Command-line interface (CLI) for validation
- ✅ Pretty-printer: reformat messy JSON into readable form

---

## 🧑‍💻 Author
Created with 💻 by [Oussama El-Asri](https://github.com/Worcrow)
---
> Feel free to use or fork. This is a learning project and a great deep-dive into how data parsing really works!
