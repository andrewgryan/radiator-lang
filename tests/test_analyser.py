import radiator


def test_analyser_given_undefined_variable():
    code = "main :: () -> u8 { x }"
    ast = radiator.parse(code)
    actual = radiator.analyse(ast)
    assert actual.model_dump() == {"errors": [{"msg": "undefined symbol 'x'"}]}
