import pytest
import radiator
import radiator.compiler


@pytest.mark.skip("developing lexer")
def test_compile_given_main_function():
    program = """
main {
  bar()
}

bar {
  5
}
"""
    expect = """.text
.global _start
main:
    stp fp, lr, [sp, #-16]!
    mov fp, sp
    bl bar
    mov sp, fp
    ldp fp, lr, [sp], #16
    ret

bar:
    mov x0, #5
    ret

_start:
    bl main
    ldr w8, =93
    svc #0
"""
    assert radiator.compile(program).to_aarch64() == expect
