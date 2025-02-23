from pydantic import BaseModel
from radiator.lexer import peek, consume, skip
from radiator.token import Kind, is_whitespace


class Call(BaseModel):
    identifier: str
    args: list[int]


class Expression(BaseModel):
    value: int | Call


class Block(BaseModel):
    expression: Expression


class DataType(BaseModel):
    signed: bool = True
    bits: int = 8


class Arg(BaseModel):
    identifier: str
    dtype: DataType


class Signature(BaseModel):
    identifier: str
    arg_list: list[Arg]
    return_type: DataType


class Function(BaseModel):
    signature: Signature
    block: Block


class AST(BaseModel):
    functions: list[Function]
    entry_point: Call


def parse(tokens):
    return parse_ast(tokens)


def parse_ast(tokens):
    functions = []
    while True:
        skip(tokens, is_whitespace)
        if peek(tokens) is None:
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
    arg_list = []
    identifier = parse_identifier(tokens)
    skip(tokens, is_whitespace)
    consume(tokens)  # :
    consume(tokens)  # :
    skip(tokens, is_whitespace)
    consume(tokens)  # (
    while peek(tokens).char != ")":
        arg = parse_arg(tokens)
        arg_list.append(arg)
        skip(tokens, is_whitespace)
        if peek(tokens).char == ",":
            consume(tokens)  # ,
            skip(tokens, is_whitespace)

    assert consume(tokens).char == ")"
    skip(tokens, is_whitespace)
    assert consume(tokens).char == "-"
    assert consume(tokens).char == ">"
    skip(tokens, is_whitespace)

    return_type = parse_dtype(tokens)
    return Signature(identifier=identifier, arg_list=arg_list, return_type=return_type)


def parse_arg(tokens):
    identifier = parse_identifier(tokens)
    skip(tokens, is_whitespace)
    skip(tokens, lambda tok: tok.char == ":")
    skip(tokens, is_whitespace)
    dtype = parse_dtype(tokens)
    return Arg(identifier=identifier, dtype=dtype)


def parse_dtype(tokens):
    signed = consume(tokens).char == "i"
    bits = parse_number(tokens)
    return DataType(signed=signed, bits=bits)


def parse_identifier(tokens):
    id = ""
    while peek(tokens) and peek(tokens).kind == Kind.letter:
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
        identifier = parse_identifier(tokens)
        if peek(tokens).char == "(":
            value = parse_call(identifier, tokens)
        else:
            value = identifier
    return Expression(value=value)


def assert_next(tokens, char):
    found = peek(tokens).char
    assert found == char, f"Expected '{char}' found '{found}' instead."


def parse_call(identifier, tokens):
    assert_next(tokens, "(")
    consume(tokens)
    args = parse_call_args(tokens)
    assert_next(tokens, ")")
    consume(tokens)
    return Call(identifier=identifier, args=args)


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
