import pytest

from rua.scanner import ScanError, Scanner
from rua.tokens import TokenType


def scan_types(source: str) -> list[TokenType]:
    return [token.type for token in Scanner(source).scan_tokens()]


def test_scans_documented_example_program() -> None:
    source = """import "pet";

global hunger = 0;

function feed():
    hunger = 0;
end
"""

    expected = [
        TokenType.IMPORT,
        TokenType.STRING,
        TokenType.SEMICOLON,
        TokenType.GLOBAL,
        TokenType.IDENTIFIER,
        TokenType.EQUAL,
        TokenType.INTEGER,
        TokenType.SEMICOLON,
        TokenType.FUNCTION,
        TokenType.IDENTIFIER,
        TokenType.LEFT_PAREN,
        TokenType.RIGHT_PAREN,
        TokenType.COLON,
        TokenType.IDENTIFIER,
        TokenType.EQUAL,
        TokenType.INTEGER,
        TokenType.SEMICOLON,
        TokenType.END,
        TokenType.EOF,
    ]

    assert scan_types(source) == expected


def test_ignores_line_comments() -> None:
    source = """global hunger = 0; // initial value
// whole line comment
hunger = hunger + 1;
"""

    expected = [
        TokenType.GLOBAL,
        TokenType.IDENTIFIER,
        TokenType.EQUAL,
        TokenType.INTEGER,
        TokenType.SEMICOLON,
        TokenType.IDENTIFIER,
        TokenType.EQUAL,
        TokenType.IDENTIFIER,
        TokenType.PLUS,
        TokenType.INTEGER,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]

    assert scan_types(source) == expected


def test_scans_string_integer_identifier_and_keywords() -> None:
    tokens = Scanner('let label = "PET"; let x = 42;').scan_tokens()

    assert tokens[0].type is TokenType.LET
    assert tokens[1].type is TokenType.IDENTIFIER
    assert tokens[1].literal == "label"
    assert tokens[3].type is TokenType.STRING
    assert tokens[3].literal == "PET"
    assert tokens[8].type is TokenType.INTEGER
    assert tokens[8].literal == 42


def test_scans_multi_character_operators() -> None:
    source = "a == b != c <= d >= e .. f"

    expected = [
        TokenType.IDENTIFIER,
        TokenType.EQUAL_EQUAL,
        TokenType.IDENTIFIER,
        TokenType.BANG_EQUAL,
        TokenType.IDENTIFIER,
        TokenType.LESS_EQUAL,
        TokenType.IDENTIFIER,
        TokenType.GREATER_EQUAL,
        TokenType.IDENTIFIER,
        TokenType.DOT_DOT,
        TokenType.IDENTIFIER,
        TokenType.EOF,
    ]

    assert scan_types(source) == expected


def test_tracks_token_line_and_column() -> None:
    tokens = Scanner("global x = 1;\n  let y = 2;").scan_tokens()

    let_token = next(token for token in tokens if token.type is TokenType.LET)
    y_token = next(token for token in tokens if token.lexeme == "y")

    assert let_token.line == 2
    assert let_token.column == 3
    assert y_token.line == 2
    assert y_token.column == 7


def test_raises_for_unterminated_string() -> None:
    with pytest.raises(ScanError, match="Unterminated string literal"):
        Scanner('let label = "PET').scan_tokens()


def test_raises_for_unknown_character() -> None:
    with pytest.raises(ScanError, match="Unexpected character '@'"):
        Scanner("@").scan_tokens()
