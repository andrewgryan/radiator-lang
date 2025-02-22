from pydantic import BaseModel
from typing import Union
from radiator.lexer import peek, consume, skip
from radiator.token import is_whitespace, Kind


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
