from pydantic import BaseModel
from typing import Union
from radiator.lexer import peek, consume, skip
from radiator.token import is_whitespace, Kind


class Operator(BaseModel):
    operation: str
    associative: str
    precedence: int

    @classmethod
    def addition(cls):
        return cls(operation="+", associative="both", precedence=1)


class BinaryOperation(BaseModel):
    lhs: Union[int, str, "BinaryOperation"]
    rhs: Union[int, str, "BinaryOperation"]
    op: Operator


def parse_atom(tokens):
    return consume(tokens).char


def parse_operator(tokens):
    c = consume(tokens).char
    if c == "+":
        return Operator.addition()
    else:
        raise Exception(f"unrecognised operator: '{c}'")


def parse_addition(tokens):
    lhs = parse_atom(tokens)
    skip(tokens, is_whitespace)
    if peek(tokens) and peek(tokens).kind == Kind.operator:
        op = parse_operator(tokens)
        skip(tokens, is_whitespace)
        rhs = parse_addition(tokens)
        return BinaryOperation(lhs=lhs, op=op, rhs=rhs)
    else:
        return lhs
