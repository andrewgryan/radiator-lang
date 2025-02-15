import itertools


class Lex:
    def __init__(self, s):
        self.s = s
        self.i = 0

    def peek(self):
        try:
            return self.s[self.i]
        except IndexError:
            pass

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

