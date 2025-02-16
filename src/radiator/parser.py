from pydantic import BaseModel
from radiator.lexer import peek, consume
from radiator.token import Kind


class Expression(BaseModel):
    value: int


def parse_expression(tokens):
    value = parse_number(tokens)
    return Expression(value=value)


def parse_number(tokens):
    result = 0
    while peek(tokens) and peek(tokens).kind == Kind.digit:
        token = consume(tokens)
        result *= 10
        result += int(token.char)
    return result


def skip(tokens, is_skippable):
    while is_skippable(peek(tokens)):
        consume(tokens)
