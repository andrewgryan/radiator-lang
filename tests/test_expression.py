from typing import Union
from radiator.lexer import lex, peek, consume, skip
from radiator.token import is_whitespace, Kind
from pydantic import BaseModel


class BinaryOperation(BaseModel):
    lhs: Union[int, str, "BinaryOperation"]
    rhs: Union[int, str, "BinaryOperation"]
    op: str


def parse_atom(tokens):
    return consume(tokens).char


def parse_operator(tokens):
    return consume(tokens).char


def parse_addition(tokens):
    lhs = parse_atom(tokens)
    skip(tokens, is_whitespace)
    if peek(tokens) and peek(tokens).kind == Kind.operator:
        op = parse_operator(tokens)
        skip(tokens, is_whitespace)
        rhs = parse_addition(tokens)
        return BinaryOperation(
            lhs=lhs, op=op, rhs=rhs
        )
    else:
        return lhs


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
