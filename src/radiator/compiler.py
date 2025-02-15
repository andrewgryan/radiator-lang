# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pydantic",
#     "typer",
# ]
# ///
import radiator
from enum import Enum
import typer
from pydantic import BaseModel

app = typer.Typer()


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
    for token in tokens:
        if token.kind == Kind.letter:
            id += token.char
        else:
            break
    return id, tokens
