from pydantic import BaseModel
from typing import Union
from radiator.lexer import peek, consume, skip
from radiator.token import is_whitespace, Kind
from radiator.parser import parse_identifier, parse_number


MIN_PRECEDENCE = 1
MAX_PRECEDENCE = 4


class Operator(BaseModel):
    operation: str
    associative: str
    precedence: int

    @classmethod
    def addition(cls):
        return cls(operation="+", associative="both", precedence=1)

    @classmethod
    def multiplication(cls):
        return cls(operation="*", associative="both", precedence=2)

    @classmethod
    def exponentiation(cls):
        return cls(operation="^", associative="right", precedence=3)


class BinaryOperation(BaseModel):
    lhs: Union[int, str, "BinaryOperation"]
    rhs: Union[int, str, "BinaryOperation"]
    op: Operator


def parse_atom(tokens):
    if peek(tokens).kind == Kind.digit:
        return parse_number(tokens)
    else:
        return parse_identifier(tokens)


def parse_operator(tokens):
    c = consume(tokens).char
    return to_operator(c)


def peek_operator(tokens):
    c = peek(tokens).char
    return to_operator(c)


def to_operator(c):
    if c == "+":
        return Operator.addition()
    elif c == "*":
        return Operator.multiplication()
    elif c == "^":
        return Operator.exponentiation()
    else:
        raise Exception(f"unrecognised operator: '{c}'")


def parse_expression(tokens, precedence=MIN_PRECEDENCE):
    if precedence >= MAX_PRECEDENCE:
        skip(tokens, is_whitespace)
        atom = parse_atom(tokens)
        return atom

    lhs = parse_expression(tokens, precedence + 1)
    skip(tokens, is_whitespace)
    if peek(tokens) and peek(tokens).kind == Kind.operator:
        skip(tokens, is_whitespace)
        op = peek_operator(tokens)
        if op.precedence == precedence:
            op = parse_operator(tokens)
            rhs = parse_expression(tokens, precedence=precedence)
            return BinaryOperation(lhs=lhs, op=op, rhs=rhs)
        else:
            return lhs
    else:
        return lhs
