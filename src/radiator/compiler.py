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


def parse(tokens):
    return AST.parse(tokens)
