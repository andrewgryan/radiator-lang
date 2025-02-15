import itertools
import pytest

class Lex:
    def __init__(self, s):
        self.s = s
        self.i = 0

    def peek(self):
        return self.s[self.i]

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= len(self.s):
            raise StopIteration
        token = self.s[self.i]
        self.i += 1
        return token


def lex(s: str):
    return Lex(s)


def peek(tokens):
    return tokens.peek()


def consume(tokens):
    return next(tokens)


def test_peek():
    tokens = lex("word")
    assert peek(tokens) == "w"
    assert peek(tokens) == "w"
    assert consume(tokens) == "w"
    assert peek(tokens) == "o"
    assert consume(tokens) == "o"
    assert peek(tokens) == "r"
    assert consume(tokens) == "r"
    assert consume(tokens) == "d"
    with pytest.raises(StopIteration):
        consume(tokens)
