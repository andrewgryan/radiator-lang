from enum import Enum
from pydantic import BaseModel


class Kind(str, Enum):
    newline = "\n"
    semicolon = ";"
    space = " "
    doublequote = '"'
    tab = "\t"
    letter = "a-z"
    digit = "0-9"
    unknown = ""
    open_brace = "{"
    close_brace = "}"
    open_paren = "("
    close_paren = ")"


class Token(BaseModel):
    char: str
    kind: Kind


def to_token(c: str):
    if any(k.value == c for k in Kind):
        return Token(char=c, kind=Kind(c))
    elif c.isalpha():
        return Token(char=c, kind=Kind.letter)
    elif c.isdigit():
        return Token(char=c, kind=Kind.digit)
    else:
        return Token(char=c, kind=Kind.unknown)
