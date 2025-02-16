from radiator.lexer import peek, consume


def skip(tokens, kind):
    while peek(tokens).kind == kind:
        consume(tokens)
