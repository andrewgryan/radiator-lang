from typing import Union
from radiator.lexer import lex
from pydantic import BaseModel


class BinaryOperation(BaseModel):
    lhs: Union[int, str, "BinaryOperation"]
    rhs: Union[int, str, "BinaryOperation"]
    op: str


def parse_addition(tokens):
    return BinaryOperation(
        lhs="a", op="+", rhs=BinaryOperation(lhs="b", op="+", rhs="c")
    )


def test_parse_addition():
    text = "a + b + c"
    actual = parse_addition(lex(text))
    assert actual.lhs == "a"
    assert actual.op == "+"
    assert actual.rhs.lhs == "b"
    assert actual.rhs.op == "+"
    assert actual.rhs.rhs == "c"
