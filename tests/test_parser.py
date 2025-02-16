from radiator.compiler import lex
from radiator.token import is_whitespace
from radiator.lexer import peek
from radiator.parser import skip, parse_expression


def test_skip_whitespace():
    tokens = lex("  \t\na")
    skip(tokens, is_whitespace)
    assert peek(tokens).char == "a"


def test_parse_expression():
    text = "42"
    actual = parse_expression(lex(text))
    assert actual.value == 42
