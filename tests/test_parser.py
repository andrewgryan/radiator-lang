import pytest
import radiator
from radiator.token import is_whitespace
from radiator.lexer import peek, lex
from radiator.parser import (
    skip,
    parse_block,
    parse_function,
    parse_ast,
)
from radiator import parser
from radiator.expression import parse_expression


def test_parse():
    code = ""
    assert radiator.parse(code).model_dump() == {
        "entry_point": {
            "args": [],
            "identifier": "main"
        },
        "functions": []
    }


def test_skip_whitespace():
    tokens = lex("  \t\na")
    skip(tokens, is_whitespace)
    assert peek(tokens).char == "a"


def test_parse_expression_given_number():
    text = "42"
    actual = parse_expression(lex(text))
    assert actual == 42


def test_parse_expression_given_call():
    text = "bar()"
    actual = parse_expression(lex(text))
    assert actual.identifier == "bar"


def test_parse_expression_given_call_arg():
    text = "bar(42)"
    actual = parse_expression(lex(text))
    assert actual.identifier == "bar"
    assert actual.args[0] == 42


def test_parse_block():
    text = "{  42  }"
    actual = parse_block(lex(text))
    assert actual.expression == 42


def test_parse_block_given_statements():
    text = "{  x: u8 = 42; x  }"
    actual = parse_block(lex(text))
    assert actual.model_dump() == {
        "statements": [],
        "expression": "x"
    }

def test_parse_statement():
    text = "x: u8 = 42;"
    actual = parser.parse_statement(lex(text))
    assert actual.model_dump() == {
        "variable": {
            "identifier": "x",
            "type": {
                "signed": False,
                "bits": 8
            }
        },
        "expression": 42
    }
    

def test_parse_function():
    text = "main :: () -> u8 {  42  }"
    actual = parse_function(lex(text))
    assert actual.signature.identifier == "main"
    assert actual.block.expression == 42


def test_parse_ast():
    text = "main :: () -> u8 {  42  }"
    actual = parse_ast(lex(text))
    assert actual.functions[0].signature.identifier == "main"
    assert actual.functions[0].block.expression == 42


def test_parse_ast_given_multiple_functions():
    text = """
main :: () -> u8 {
  bar()
}

bar :: () -> u8 {
  5
}
"""
    actual = parse_ast(lex(text))
    assert actual.functions[0].signature.identifier == "main"
    assert actual.functions[0].block.expression.identifier == "bar"
    assert actual.functions[1].signature.identifier == "bar"
    assert actual.functions[1].block.expression == 5


def test_parse_ast_given_comment():
    text = """
    // MAIN
    //
    // A program that exits with status 0
    main :: () -> u8 {
        0
    }
    """
    actual = parse_ast(lex(text))
    assert actual.model_dump() == {
        "entry_point": {
            "args": [],
            "identifier": "main"
        },
        "functions": [{
            "block": {
                "expression": 0, 
                "statements": []
            },
            "signature":{
                "identifier": "main",
                "parameters": [],
                "return_type": {
                    "bits": 8,
                    "signed": False
                }
            }
        }]
    }


def test_parse_signature():
    text = "name :: () -> u8"
    actual = parser.parse_signature(lex(text))
    assert actual.identifier == "name"
    assert actual.parameters == []
    assert actual.return_type.signed == False
    assert actual.return_type.bits == 8


def test_parse_signature_given_args():
    text = "name :: (x: i32) -> i32"
    actual = parser.parse_signature(lex(text))
    assert actual.parameters[0].identifier == "x"
    assert actual.parameters[0].dtype.signed == True
    assert actual.parameters[0].dtype.bits == 32


@pytest.mark.parametrize(
    "code,expected",
    [
        (
            "name :: (x: i32, y: i32) -> i32",
            {
                "identifier": "name",
                "parameters": [
                    {"dtype": {"bits": 32, "signed": True}, "identifier": "x"},
                    {"dtype": {"bits": 32, "signed": True}, "identifier": "y"},
                ],
                "return_type": {"bits": 32, "signed": True},
            },
        ),
        (
            "name :: (a_b: i32) -> i32",
            {
                "identifier": "name",
                "parameters": [
                    {"dtype": {"bits": 32, "signed": True}, "identifier": "a_b"},
                ],
                "return_type": {"bits": 32, "signed": True},
            },
        ),
        (
            "x0 :: () -> i32",
            {
                "identifier": "x0",
                "parameters": [],
                "return_type": {"bits": 32, "signed": True},
            },
        ),
    ],
)
def test_parse_signature_given_multiple_args(code, expected):
    text = "name :: (x: i32, y: i32) -> i32"
    actual = parser.parse_signature(lex(code))
    assert actual.model_dump() == expected


def test_parse_dtype():
    text = "u32"
    actual = parser.parse_dtype(lex(text))
    assert actual.signed == False
    assert actual.bits == 32


def test_parse_parameter_given_u8():
    text = "x :: u8"
    actual = parser.parse_parameter(lex(text))
    assert actual.identifier == "x"
    assert actual.dtype.signed == False
    assert actual.dtype.bits == 8


def test_parse_parameter_given_i16():
    text = "y :: i16"
    actual = parser.parse_parameter(lex(text))
    assert actual.identifier == "y"
    assert actual.dtype.signed == True
    assert actual.dtype.bits == 16


@pytest.mark.parametrize("code,expected", [
    ("// Comment!", {"text": " Comment!"}),
    ("// Comment!\ny :: i16", {"text": " Comment!"})
])
def test_parse_comment(code, expected):
    actual = parser.parse_comment(lex(code))
    assert actual.model_dump() == expected
