from rua.tokens import KEYWORDS, Token, TokenType


def test_keywords_table_matches_rua_v1_keywords() -> None:
    expected_keywords = {
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

    assert KEYWORDS == expected_keywords


def test_token_stores_location_and_literal_data() -> None:
    token = Token(
        type=TokenType.STRING,
        lexeme='"PET"',
        literal="PET",
        line=3,
        column=8,
    )

    assert token.type is TokenType.STRING
    assert token.lexeme == '"PET"'
    assert token.literal == "PET"
    assert token.line == 3
    assert token.column == 8


def test_token_type_covers_current_rua_v1_grammar() -> None:
    expected_types = {
        "LEFT_PAREN",
        "RIGHT_PAREN",
        "COMMA",
        "COLON",
        "SEMICOLON",
        "EQUAL",
        "PLUS",
        "MINUS",
        "STAR",
        "SLASH",
        "LESS",
        "GREATER",
        "EQUAL_EQUAL",
        "BANG_EQUAL",
        "LESS_EQUAL",
        "GREATER_EQUAL",
        "DOT_DOT",
        "IDENTIFIER",
        "INTEGER",
        "STRING",
        "IMPORT",
        "FUNCTION",
        "LET",
        "GLOBAL",
        "IF",
        "THEN",
        "ELSE",
        "WHILE",
        "DO",
        "FOR",
        "IN",
        "RETURN",
        "TRUE",
        "FALSE",
        "AND",
        "OR",
        "NOT",
        "END",
        "VERIFY",
        "EXTERN",
        "EOF",
    }

    assert {token_type.name for token_type in TokenType} == expected_types
