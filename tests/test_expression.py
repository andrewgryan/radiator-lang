from radiator.lexer import lex
from radiator.expression import parse_addition


def test_parse_addition_basic():
    text = "a + b"
    actual = parse_addition(lex(text))
    assert actual.lhs == "a"
    assert actual.op == "+"
    assert actual.rhs == "b"


def test_parse_addition_associative():
    text = "a + b + c"
    actual = parse_addition(lex(text))
    assert actual.lhs == "a"
    assert actual.op == "+"
    assert actual.rhs.lhs == "b"
    assert actual.rhs.op == "+"
    assert actual.rhs.rhs == "c"
