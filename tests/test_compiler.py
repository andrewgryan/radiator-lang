import radiator


def test_compile():
    expect = """.text
.global _start
_start:
    ldr w8, #93
    ldr x0, #0
    svc #0"""
    assert radiator.compile("").to_aarch64() == expect
