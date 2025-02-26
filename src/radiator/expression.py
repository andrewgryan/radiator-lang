from pydantic import BaseModel
from typing import Union
from radiator.lexer import peek, consume, skip, assert_next
from radiator.token import is_whitespace, Kind


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
    lhs: Union[int, str, "Call", "BinaryOperation"]
    rhs: Union[int, str, "Call", "BinaryOperation"]
    op: Operator


class Call(BaseModel):
    identifier: str
    args: list[Union[str, int, "Call"]]


Expression = Union[str, int, Call, BinaryOperation]


def peek_atom(tokens):
    tok = peek(tokens)
    return (tok.kind == Kind.digit) or (tok.kind == Kind.letter)


def parse_atom(tokens):
    if peek(tokens).kind == Kind.digit:
        return parse_number(tokens)
    else:
        # Expression in ()
        if peek(tokens) and peek(tokens).char == "(":
            assert_next(tokens, "(")
            consume(tokens)
            value = parse_expression(tokens)
            skip(tokens, is_whitespace)
            assert_next(tokens, ")")
            consume(tokens)
            return value

        # Identifier OR function call()
        identifier = parse_identifier(tokens)
        if peek(tokens) and peek(tokens).char == "(":
            assert_next(tokens, "(")
            consume(tokens)
            args = parse_call_args(tokens, parse_arg=parse_atom, peek_fn=peek_atom)
            assert_next(tokens, ")")
            consume(tokens)
            return Call(identifier=identifier, args=args)
        else:
            return identifier


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


# Parser functions


def parse_identifier(tokens):
    id = ""
    while peek(tokens):
        token = peek(tokens)
        if (token.kind == Kind.letter) or (token.kind == Kind.underscore):
            id += consume(tokens).char
        elif token.kind == Kind.digit:
            id += consume(tokens).char
        else:
            break
    return id


def parse_number(tokens):
    result = 0
    while peek(tokens) and peek(tokens).kind == Kind.digit:
        token = consume(tokens)
        result *= 10
        result += int(token.char)
    return result


def peek_number(tokens):
    return peek(tokens).kind == Kind.digit


def parse_call_args(tokens, parse_arg=parse_number, peek_fn=peek_number):
    args = []
    while peek(tokens):
        if peek_fn(tokens):
            args.append(parse_arg(tokens))
            if peek(tokens).kind == Kind.comma:
                consume(tokens)
                skip(tokens, is_whitespace)
        else:
            break
    return args
