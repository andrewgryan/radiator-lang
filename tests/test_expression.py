import pytest
from radiator.lexer import lex
from radiator.expression import (
    parse_addition,
    parse_operator,
)


@pytest.mark.parametrize(
    "text,expected", [
        ("+", {"associative": "both", "operation": "+", "precedence": 1}),
        ("*", {"associative": "both", "operation": "*", "precedence": 2}),
    ]
)
def test_parse_operator(text, expected):
    assert parse_operator(lex(text)).model_dump() == expected


@pytest.mark.parametrize(
    "text,expected",
    [
        pytest.param(
            "a + b + c",
            {
                "lhs": "a",
                "op": {"associative": "both", "operation": "+", "precedence": 1},
                "rhs": {
                    "lhs": "b",
                    "op": {"associative": "both", "operation": "+", "precedence": 1},
                    "rhs": "c",
                },
            },
        ),
        pytest.param(
            "a + b",
            {
                "lhs": "a",
                "op": {"associative": "both", "operation": "+", "precedence": 1},
                "rhs": "b",
            },
        ),
    ],
)
def test_parse_addition_associative(text, expected):
    actual = parse_addition(lex(text))
    assert actual.model_dump() == expected
