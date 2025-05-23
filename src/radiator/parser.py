from pydantic import BaseModel
from radiator.lexer import peek, consume, skip, assert_next
from radiator.token import Token, Kind, is_whitespace
from radiator.expression import (
    parse_expression,
    Expression,
    parse_identifier,
    parse_number,
    Call,
)


class Comment(BaseModel):
    text: str


class DataType(BaseModel):
    signed: bool = True
    bits: int = 8


class Variable(BaseModel):
    identifier: str
    type: DataType


class Assignment(BaseModel):
    variable: Variable
    expression: Expression


Statement = Assignment


class Block(BaseModel):
    statements: list[Statement]
    expression: Expression


class Parameter(BaseModel):
    identifier: str
    dtype: DataType


class Signature(BaseModel):
    identifier: str
    parameters: list[Parameter]
    return_type: DataType


class Function(BaseModel):
    signature: Signature
    block: Block


class AST(BaseModel):
    functions: list[Function]
    entry_point: Call


def parse_ast(tokens):
    functions = []
    while True:
        skip(tokens, is_whitespace)
        if peek(tokens) is None:
            break
        while True:
            comment = parse_comment(tokens)
            skip(tokens, is_whitespace)
            if comment is None:
                break
        function = parse_function(tokens)
        if isinstance(function, Function):
            functions.append(function)
        else:
            break
    entry_point = Call(identifier="main", args=[])
    return AST(functions=functions, entry_point=entry_point)


def parse_function(tokens):
    signature = parse_signature(tokens)
    skip(tokens, is_whitespace)
    block = parse_block(tokens)
    return Function(signature=signature, block=block)


def parse_signature(tokens):
    parameters = []
    identifier = parse_identifier(tokens)
    skip(tokens, is_whitespace)
    assert_next(tokens, ":")
    consume(tokens)
    assert_next(tokens, ":")
    consume(tokens)
    skip(tokens, is_whitespace)
    assert_next(tokens, "(")
    consume(tokens)
    while peek(tokens).char != ")":
        parameters.append(parse_parameter(tokens))
        skip(tokens, is_whitespace)
        if peek(tokens).char == ",":
            consume(tokens)  # ,
            skip(tokens, is_whitespace)

    assert_next(tokens, ")")
    consume(tokens)
    skip(tokens, is_whitespace)
    assert_next(tokens, "-")
    consume(tokens)
    assert_next(tokens, ">")
    consume(tokens)
    skip(tokens, is_whitespace)

    return_type = parse_dtype(tokens)
    return Signature(
        identifier=identifier, parameters=parameters, return_type=return_type
    )


def parse_parameter(tokens):
    identifier = parse_identifier(tokens)
    skip(tokens, is_whitespace)
    skip(tokens, lambda tok: tok.char == ":")
    skip(tokens, is_whitespace)
    dtype = parse_dtype(tokens)
    return Parameter(identifier=identifier, dtype=dtype)


def parse_dtype(tokens):
    signed = consume(tokens).char == "i"
    bits = parse_number(tokens)
    return DataType(signed=signed, bits=bits)


def parse_block(tokens):
    if peek(tokens).kind == Kind.open_brace:
        consume(tokens)
    else:
        return
    skip(tokens, is_whitespace)
    statements = parse_statements(tokens)
    skip(tokens, is_whitespace)
    expression = parse_expression(tokens)
    skip(tokens, is_whitespace)
    if peek(tokens).kind == Kind.close_brace:
        consume(tokens)
    else:
        pass  # TODO: syntax error handling
    return Block(expression=expression, statements=statements)


def parse_statements(tokens):
    return []


def parse_statement(tokens):
    return parse_assignment(tokens)


def parse_assignment(tokens):
    identifier = parse_identifier(tokens)
    skip(tokens, is_whitespace)
    skip(tokens, lambda tok: tok.char == ":")
    skip(tokens, is_whitespace)
    dtype = parse_dtype(tokens)
    skip(tokens, is_whitespace)
    assert_next(tokens, "=")
    consume(tokens)
    skip(tokens, is_whitespace)
    expression = parse_expression(tokens)
    return Assignment(
        variable=Variable(identifier=identifier, type=dtype),
        expression=expression,
    )


def parse_comment(tokens: [Token]) -> Comment | None:
    slashes = 0
    while peek(tokens) and peek(tokens).char == "/":
        slashes += 1
        consume(tokens)
    if slashes >= 2:
        text = ""
        while peek(tokens) and peek(tokens).char != "\n":
            text += consume(tokens).char
        return Comment(text=text)
