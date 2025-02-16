from radiator.compiler import lex
from radiator.token import Kind
from radiator.lexer import peek
from radiator.parser import skip


def test_skip_whitespace():
    tokens = lex("    a")
    skip(tokens, Kind.space)
    assert peek(tokens).char == "a"
