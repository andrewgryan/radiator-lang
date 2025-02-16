from pydantic import BaseModel
from radiator.lexer import peek, consume
from radiator.token import Kind, is_whitespace


class Call(BaseModel):
    identifier: str


class Expression(BaseModel):
    value: int | Call


class Block(BaseModel):
    expression: Expression


class Function(BaseModel):
    identifier: str
    block: Block


class AST(BaseModel):
    functions: list[Function]
    entry_point: Call

    @classmethod
    def parse(cls, tokens):
        functions = []
        return cls(functions=functions, entry_point=Call(identifier="main"))


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
    if peek(tokens).kind == Kind.digit:
        value = parse_number(tokens)
    else:
        value = parse_call(tokens)
    return Expression(value=value)


def parse_call(tokens):
    identifier = parse_identifier(tokens)
    consume(tokens)
    consume(tokens)
    return Call(identifier=identifier)


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
