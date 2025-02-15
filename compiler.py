# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pydantic",
#     "typer",
# ]
# ///
from enum import Enum
import typer
from pydantic import BaseModel


class Kind(str, Enum):
    newline = "\n"
    semicolon = ";"
    space = " "
    doublequote = "\""
    tab = "\t"
    letter = "a-z"
    unknown = ""
    open_brace = "{"
    close_brace = "}"
    open_paren = "("
    close_paren = ")"


class Token(BaseModel):
    char: str
    kind: Kind


def main(script: str) -> None:
    with open(script, "r") as stream:
        tree = parse(lex(stream.read()))
        print(tree)


def lex(text):
    for c in text:
        if any(k.value == c for k in Kind):
            yield Token(char=c, kind=Kind(c))
        elif c.isalpha():
            yield Token(char=c, kind=Kind.letter)
        else:
            yield Token(char=c, kind=Kind.unknown)


def parse(tokens):
    id, tokens = parse_identifier(tokens)
    return id


def parse_identifier(tokens):
    id = ""
    token = next(tokens)
    while token.kind == Kind.letter:
        id += token.char
        token = next(tokens)
    return id, tokens


if __name__ == "__main__":
    typer.run(main)
