import pytest
from radiator.compiler import lex
from radiator.token import is_whitespace
from radiator.lexer import peek
from radiator.parser import (
    skip,
    parse_expression,
    parse_block,
    parse_function,
    parse_ast,
)
from radiator import parser


def test_skip_whitespace():
    tokens = lex("  \t\na")
    skip(tokens, is_whitespace)
    assert peek(tokens).char == "a"


def test_parse_expression_given_number():
    text = "42"
    actual = parse_expression(lex(text))
    assert actual.value == 42


def test_parse_expression_given_call():
    text = "bar()"
    actual = parse_expression(lex(text))
    assert actual.value.identifier == "bar"


def test_parse_block():
    text = "{  42  }"
    actual = parse_block(lex(text))
    assert actual.expression.value == 42


def test_parse_function():
    text = "main :: () -> u8 {  42  }"
    actual = parse_function(lex(text))
    assert actual.signature.identifier == "main"
    assert actual.block.expression.value == 42


def test_parse_ast():
    text = "main :: () -> u8 {  42  }"
    actual = parse_ast(lex(text))
    assert actual.functions[0].signature.identifier == "main"
    assert actual.functions[0].block.expression.value == 42


def test_parse_ast_given_multiple_functions():
    text = """
main :: () -> u8 {
  bar(5)
}

bar :: (x: u8) -> u8 {
  x
}
"""
    actual = parse_ast(lex(text))
    assert actual.functions[0].signature.identifier == "main"
    assert actual.functions[0].block.expression.value.identifier == "bar"
    assert actual.functions[1].signature.identifier == "bar"
    assert actual.functions[1].block.expression.value == 5


def test_parse_signature():
    text = "name :: () -> u8"
    actual = parser.parse_signature(lex(text))
    assert actual.identifier == "name"
    assert actual.arg_list == []
    assert actual.return_type.signed == False
    assert actual.return_type.bits == 8


def test_parse_signature_given_args():
    text = "name :: (x: i32) -> i32"
    actual = parser.parse_signature(lex(text))
    assert actual.arg_list[0].identifier == "x"
    assert actual.arg_list[0].dtype.signed == True
    assert actual.arg_list[0].dtype.bits == 32


def test_parse_signature_given_multiple_args():
    text = "name :: (x: i32, y: i32) -> i32"
    actual = parser.parse_signature(lex(text))
    assert actual.arg_list[0].identifier == "x"
    assert actual.arg_list[0].dtype.signed == True
    assert actual.arg_list[0].dtype.bits == 32
    assert actual.arg_list[1].identifier == "y"
    assert actual.arg_list[1].dtype.signed == True
    assert actual.arg_list[1].dtype.bits == 32


def test_parse_dtype():
    text = "u32"
    actual = parser.parse_dtype(lex(text))
    assert actual.signed == False
    assert actual.bits == 32


def test_parse_arg_given_u8():
    text = "x :: u8"
    actual = parser.parse_arg(lex(text))
    assert actual.identifier == "x"
    assert actual.dtype.signed == False
    assert actual.dtype.bits == 8


def test_parse_arg_given_i16():
    text = "y :: i16"
    actual = parser.parse_arg(lex(text))
    assert actual.identifier == "y"
    assert actual.dtype.signed == True
    assert actual.dtype.bits == 16
