from radiator.compiler import lex
from radiator.token import is_whitespace
from radiator.lexer import peek
from radiator.parser import skip, parse_expression, parse_block, parse_function


def test_skip_whitespace():
    tokens = lex("  \t\na")
    skip(tokens, is_whitespace)
    assert peek(tokens).char == "a"


def test_parse_expression():
    text = "42"
    actual = parse_expression(lex(text))
    assert actual.value == 42


def test_parse_block():
    text = "{  42  }"
    actual = parse_block(lex(text))
    assert actual.expression.value == 42


def test_parse_function():
    text = "main {  42  }"
    actual = parse_function(lex(text))
    assert actual.identifier == "main"
    assert actual.block.expression.value == 42
