import radiator
import pytest


@pytest.mark.parametrize(
    "code,expected",
    [
        ("main :: () -> u8 { x }", {"errors": [{"msg": "undefined symbol 'x'"}]}),
        ("main :: () -> u8 { 0 }", {"errors": []}),
    ],
)
def test_analyser_given_undefined_variable(code, expected):
    ast = radiator.parse(code)
    actual = radiator.analyse(ast)
    assert actual.model_dump() == expected
