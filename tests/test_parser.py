from radiator.compiler import lex
from radiator.token import is_whitespace
from radiator.lexer import peek
from radiator.parser import skip


def test_skip_whitespace():
    tokens = lex("  \t\na")
    skip(tokens, is_whitespace)
    assert peek(tokens).char == "a"
