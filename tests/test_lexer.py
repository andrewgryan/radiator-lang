import pytest
from radiator.lexer import lex, peek, consume

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
    assert peek(tokens) is None
    with pytest.raises(StopIteration):
        consume(tokens)
