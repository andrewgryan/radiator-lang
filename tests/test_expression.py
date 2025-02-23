import pytest
from radiator.lexer import lex
from radiator.expression import (
    parse_expression,
    parse_operator,
    parse_atom
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
    "text,expected", [
        ("a", "a"),
        ("foo", "foo"),
        ("123", 123),
        ("fn()", {"args": [], "identifier": "fn"}),
        ("foo(1, 2)", {"args": [1, 2], "identifier": "foo"})
    ]
)
def test_parse_atom(text, expected):
    atom = parse_atom(lex(text))
    if hasattr(atom, "model_dump"):
        assert atom.model_dump() == expected
    else:
        assert atom == expected


@pytest.mark.parametrize(
    "text,expected",
    [
        pytest.param(
            "a",
            "a",
            id="a",
        ),
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
            id="a + b + c",
        ),
        pytest.param(
            "a + b",
            {
                "lhs": "a",
                "op": {"associative": "both", "operation": "+", "precedence": 1},
                "rhs": "b",
            },
            id="a + b",
        ),
        pytest.param(
            "a * b",
            {
                "lhs": "a",
                "op": {"associative": "both", "operation": "*", "precedence": 2},
                "rhs": "b",
            },
            id="a * b",
        ),
        pytest.param(
            "a * b + c",
            {
                "lhs": {
                    "lhs": "a",
                    "op": {"associative": "both", "operation": "*", "precedence": 2},
                    "rhs": "b"
                },
                "op": {"associative": "both", "operation": "+", "precedence": 1},
                "rhs": "c",
            },
            id="a * b + c",
        ),
        pytest.param(
            "1 + bar", {
                "lhs": 1,
                "op": {"associative": "both", "operation": "+", "precedence": 1},
                "rhs": "bar"
            }
        )
    ],
)
def test_parse_expression_associative(text, expected):
    actual = parse_expression(lex(text))
    if isinstance(actual, str):
        assert actual == expected
    else:
        assert actual.model_dump() == expected
