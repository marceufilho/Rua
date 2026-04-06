"""Regex-driven scanner for Rua V1 source code."""

import re

from rua.tokens import KEYWORDS, Token, TokenType


class ScanError(Exception):
    """Raised when the scanner finds invalid source text."""


class Scanner:
    """Convert Rua source code into a sequence of tokens."""

    TOKEN_REGEX = re.compile(
        "|".join(
            [
                r"(?P<WHITESPACE>[ \t\r]+)",
                r"(?P<NEWLINE>\n+)",
                r"(?P<COMMENT>//[^\n]*)",
                r"(?P<EQUAL_EQUAL>==)",
                r"(?P<BANG_EQUAL>!=)",
                r"(?P<LESS_EQUAL><=)",
                r"(?P<GREATER_EQUAL>>=)",
                r"(?P<DOT_DOT>\.\.)",
                r'(?P<STRING>"[^"\n]*")',
                r"(?P<LEFT_PAREN>\()",
                r"(?P<RIGHT_PAREN>\))",
                r"(?P<COMMA>,)",
                r"(?P<COLON>:)",
                r"(?P<SEMICOLON>;)",
                r"(?P<EQUAL>=)",
                r"(?P<PLUS>\+)",
                r"(?P<MINUS>-)",
                r"(?P<STAR>\*)",
                r"(?P<SLASH>/)",
                r"(?P<LESS><)",
                r"(?P<GREATER>>)",
                r"(?P<INTEGER>\d+)",
                r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)",
            ]
        )
    )

    TOKEN_TYPES = {
        "LEFT_PAREN": TokenType.LEFT_PAREN,
        "RIGHT_PAREN": TokenType.RIGHT_PAREN,
        "COMMA": TokenType.COMMA,
        "COLON": TokenType.COLON,
        "SEMICOLON": TokenType.SEMICOLON,
        "EQUAL": TokenType.EQUAL,
        "PLUS": TokenType.PLUS,
        "MINUS": TokenType.MINUS,
        "STAR": TokenType.STAR,
        "SLASH": TokenType.SLASH,
        "LESS": TokenType.LESS,
        "GREATER": TokenType.GREATER,
        "EQUAL_EQUAL": TokenType.EQUAL_EQUAL,
        "BANG_EQUAL": TokenType.BANG_EQUAL,
        "LESS_EQUAL": TokenType.LESS_EQUAL,
        "GREATER_EQUAL": TokenType.GREATER_EQUAL,
        "DOT_DOT": TokenType.DOT_DOT,
    }

    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.start_line = 1
        self.start_column = 1

    def scan_tokens(self) -> list[Token]:
        """Scan the full source string and return all tokens."""
        while not self.is_at_end():
            self.start = self.current
            self.start_line = self.line
            self.start_column = self.column
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line, self.column))
        return self.tokens

    def scan_token(self) -> None:
        """Scan the next token from the current source position."""
        match = self.TOKEN_REGEX.match(self.source, self.current)
        if match is None:
            current_char = self.peek()
            if current_char == '"':
                self.error("Unterminated string literal.")
            if current_char == "!":
                self.error("Unexpected character '!'. Did you mean '!='?")
            self.error(f"Unexpected character {current_char!r}.")

        lexeme = match.group(0)
        kind = match.lastgroup
        self.current = match.end()

        if kind is None:
            self.error("Unknown scanner state.")

        if kind in {"WHITESPACE", "NEWLINE", "COMMENT"}:
            self.advance_position(lexeme)
            return

        literal: object | None = None

        if kind == "IDENTIFIER":
            token_type = KEYWORDS.get(lexeme, TokenType.IDENTIFIER)
            literal = None if token_type is not TokenType.IDENTIFIER else lexeme
        elif kind == "INTEGER":
            token_type = TokenType.INTEGER
            literal = int(lexeme)
        elif kind == "STRING":
            token_type = TokenType.STRING
            literal = lexeme[1:-1]
        else:
            token_type = self.TOKEN_TYPES[kind]

        self.add_token(token_type, literal)
        self.advance_position(lexeme)

    def add_token(self, token_type: TokenType, literal: object | None = None) -> None:
        lexeme = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, lexeme, literal, self.start_line, self.start_column))

    def advance_position(self, lexeme: str) -> None:
        newline_count = lexeme.count("\n")
        if newline_count == 0:
            self.column += len(lexeme)
            return

        self.line += newline_count
        self.column = len(lexeme.rsplit("\n", maxsplit=1)[-1]) + 1

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def error(self, message: str) -> None:
        raise ScanError(f"{message} Line {self.start_line}, column {self.start_column}.")
