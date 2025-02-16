# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pydantic",
#     "typer",
# ]
# ///
import radiator
from radiator.token import Token, Kind, to_token
from radiator.lexer import Lex
import typer
from pydantic import BaseModel
from typing import Optional, Self
import subprocess

app = typer.Typer()


@app.command()
def main(script: str, out: str = None) -> None:
    with open(script, "r") as stream:
        text = stream.read()
        code = radiator.compile(text).to_aarch64()
        if out:
            with open(out, "w") as stream:
                stream.write(code)
        else:
            print(code)

        # Compile assembly to executable
        status = subprocess.call(["as", "-o", "main.o", out])
        if status == 0:
            status = subprocess.call(["ld", "-o", "main", "main.o"])


def lex(s: str):
    return Lex(s).map(to_token)


class Call(BaseModel):
    identifier: str


class Function(BaseModel):
    identifier: str
    return_value: int | Call

    @classmethod
    def parse(cls, tokens: list[Token]) -> Optional[Self]:
        return_value = 0
        for token in tokens:
            if token.kind == Kind.close_brace:
                break
            elif token.kind == Kind.digit:
                return_value *= 10
                return_value += int(token.char)
        return cls(identifier="baz", return_value=return_value)


class Block(BaseModel):
    expression: str


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
    statements = parse_statements(tokens)
    if peek(tokens).kind == Kind.close_brace:
        consume(tokens)
    else:
        pass  # TODO: syntax error handling
    return Block(statements=statements)


def parse_call(tokens):
    identifier = parse_identifier(tokens)
    return Call(identifier=identifier)


class AST(BaseModel):
    functions: list[Function]
    entry_point: Call

    @classmethod
    def parse(cls, tokens):
        functions = [Function.parse(tokens), Function(identifier="foo", return_value=5)]
        return cls(functions=functions, entry_point=Call(identifier="main"))


def parse(tokens):
    return AST.parse(tokens)
