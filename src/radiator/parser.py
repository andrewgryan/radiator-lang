from radiator.lexer import peek, consume


def skip(tokens, is_skippable):
    while is_skippable(peek(tokens)):
        consume(tokens)
