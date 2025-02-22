import pytest
from radiator.lexer import lex, peek, consume


def test_peek():
    tokens = lex("word")
    assert peek(tokens).char == "w"
    assert peek(tokens).char == "w"
    assert consume(tokens).char == "w"
    assert peek(tokens).char == "o"
    assert consume(tokens).char == "o"
    assert peek(tokens).char == "r"
    assert consume(tokens).char == "r"
    assert consume(tokens).char == "d"
    assert peek(tokens) is None
    with pytest.raises(StopIteration):
        consume(tokens)
