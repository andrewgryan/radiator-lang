import radiator
import radiator.compiler


def test_compile():
    expect = """.text
.global _start
_start:
    ldr w8, =93
    ldr x0, =0
    svc #0
"""
    assert radiator.compile("").to_aarch64() == expect


def test_lex():
    assert list(radiator.compiler.lex("")) == []


def test_parse():
    given = radiator.compiler.lex("")
    assert list(radiator.compiler.parse(given)) == []
