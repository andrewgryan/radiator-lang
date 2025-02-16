from pydantic import BaseModel
from radiator.lexer import peek, consume
from radiator.token import Kind, is_whitespace


class Expression(BaseModel):
    value: int


class Block(BaseModel):
    expression: Expression


class Function(BaseModel):
    identifier: str
    block: Block


def parse_function(tokens):
    identifier = parse_identifier(tokens)
    skip(tokens, is_whitespace)
    block = parse_block(tokens)
    return Function(identifier=identifier, block=block)
    

def parse_identifier(tokens):
    id = ""
    while peek(tokens).kind == Kind.letter:
        id += consume(tokens).char
    return id


def parse_block(tokens):
    if peek(tokens).kind == Kind.open_brace:
        consume(tokens)
    else:
        return
    skip(tokens, is_whitespace)
    expression = parse_expression(tokens)
    skip(tokens, is_whitespace)
    if peek(tokens).kind == Kind.close_brace:
        consume(tokens)
    else:
        pass  # TODO: syntax error handling
    return Block(expression=expression)


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
