import pytest
from radiator.lexer import lex
from radiator.expression import parse_expression, parse_operator, parse_atom


PLUS = {"associative": "both", "operation": "+", "precedence": 1}
TIMES = {"associative": "both", "operation": "*", "precedence": 2}
POWER = {"associative": "right", "operation": "^", "precedence": 3}


@pytest.mark.parametrize(
    "text,expected",
    [
        ("+", PLUS),
        ("*", TIMES),
    ],
)
def test_parse_operator(text, expected):
    assert parse_operator(lex(text)).model_dump() == expected


@pytest.mark.parametrize(
    "text,expected",
    [
        ("a", "a"),
        ("foo", "foo"),
        ("123", 123),
        ("fn()", {"args": [], "identifier": "fn"}),
        ("foo(1, 2)", {"args": [1, 2], "identifier": "foo"}),
        (
            "foo(bar())",
            {"args": [{"args": [], "identifier": "bar"}], "identifier": "foo"},
        ),
    ],
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
                "op": PLUS,
                "rhs": {
                    "lhs": "b",
                    "op": PLUS,
                    "rhs": "c",
                },
            },
            id="a + b + c",
        ),
        pytest.param(
            "a + b",
            {
                "lhs": "a",
                "op": PLUS,
                "rhs": "b",
            },
            id="a + b",
        ),
        pytest.param(
            "a * b",
            {
                "lhs": "a",
                "op": TIMES,
                "rhs": "b",
            },
            id="a * b",
        ),
        pytest.param(
            "a * b + c",
            {
                "lhs": {
                    "lhs": "a",
                    "op": TIMES,
                    "rhs": "b",
                },
                "op": PLUS,
                "rhs": "c",
            },
            id="a * b + c",
        ),
        pytest.param(
            "1 + bar",
            {
                "lhs": 1,
                "op": PLUS,
                "rhs": "bar",
            },
        ),
        pytest.param(
            "foo() + 9",
            {
                "lhs": {"args": [], "identifier": "foo"},
                "op": PLUS,
                "rhs": 9,
            },
        ),
        pytest.param(
            "(1 + 2) * 3",
            {
                "lhs": {
                    "lhs": 1,
                    "op": PLUS,
                    "rhs": 2,
                },
                "op": TIMES,
                "rhs": 3,
            },
        ),
        pytest.param(
            "2 ^ 4",
            {
                "lhs": 2,
                "op": POWER,
                "rhs": 4
            }
        ),
        pytest.param(
            "2 ^ 3 ^ 4",
            {
                "lhs": 2,
                "op": POWER,
                "rhs": {
                    "lhs": 3,
                    "op": POWER,
                    "rhs": 4
                },
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
