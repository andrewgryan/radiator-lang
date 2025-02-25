from radiator.token import to_token


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

    def map(self, fn):
        return LexMap(self, fn)


class LexMap:
    """Higher-order lexer"""

    def __init__(self, lexer, fn):
        self.lexer = lexer
        self.fn = fn

    def peek(self):
        token = self.lexer.peek()
        if token is None:
            return
        return self.fn(token)

    def __iter__(self):
        return self

    def __next__(self):
        return self.fn(next(self.lexer))


def lex(s: str):
    return Lex(s).map(to_token)


def peek(tokens):
    return tokens.peek()


def consume(tokens):
    return next(tokens)


def skip(tokens, is_skippable):
    while peek(tokens) and is_skippable(peek(tokens)):
        consume(tokens)


def assert_next(tokens, char):
    found = peek(tokens).char
    assert found == char, f"Expected '{char}' found '{found}' instead."
