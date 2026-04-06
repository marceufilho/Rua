"""Token definitions for the Rua V1 scanner and parser."""

from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    """All token kinds supported by the Rua V1 grammar."""

    # Single-character delimiters and operators.
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    COMMA = auto()
    COLON = auto()
    SEMICOLON = auto()
    EQUAL = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    LESS = auto()
    GREATER = auto()

    # Multi-character operators.
    EQUAL_EQUAL = auto()
    BANG_EQUAL = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()
    DOT_DOT = auto()

    # Literals.
    IDENTIFIER = auto()
    INTEGER = auto()
    STRING = auto()

    # Keywords.
    IMPORT = auto()
    FUNCTION = auto()
    LET = auto()
    GLOBAL = auto()
    IF = auto()
    THEN = auto()
    ELSE = auto()
    WHILE = auto()
    DO = auto()
    FOR = auto()
    IN = auto()
    RETURN = auto()
    TRUE = auto()
    FALSE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    END = auto()
    VERIFY = auto()
    EXTERN = auto()

    EOF = auto()


@dataclass(frozen=True, slots=True)
class Token:
    """A single token produced by scanning source code."""

    type: TokenType
    lexeme: str
    literal: object | None
    line: int
    column: int


KEYWORDS = {
    "import": TokenType.IMPORT,
    "function": TokenType.FUNCTION,
    "let": TokenType.LET,
    "global": TokenType.GLOBAL,
    "if": TokenType.IF,
    "then": TokenType.THEN,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "do": TokenType.DO,
    "for": TokenType.FOR,
    "in": TokenType.IN,
    "return": TokenType.RETURN,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "not": TokenType.NOT,
    "end": TokenType.END,
    "verify": TokenType.VERIFY,
    "extern": TokenType.EXTERN,
}
