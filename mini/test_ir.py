from ir import (
    Program,
    Function,
    Loop,
    SystemCall,
    String,
    x86_64,
    aarch64,
)


def test_function_to_x86_64():
    ir = Function(
        identifier="main",
        statements=[
            SystemCall(
                "write",
                "stdout",
                "Hello, World!\n",
            )
        ],
    )
    assert x86_64(ir) == ""


def test_x86_64():
    ir = Program(main=Function(identifier="main"))
    assert (
        x86_64(ir)
        == """
    """.strip()
    )


def test_aarch64():
    s = String(
        identifier="msg", text="Hello, World!\n"
    )
    ir = Program(
        main=Function(
            identifier="main",
            statements=[
                SystemCall("write", "stdout", s)
            ],
        )
    )
    assert (
        aarch64(ir)
        == """
.data
msg:
    .ascii "Hello, World!\n"
msg_len = . - msg

.text
.global _start

main:
    stp fp, lr, [sp, #-16]!
    mov fp, sp

    mov x0, #1
    ldr x1, =msg
    ldr x2, =msg_len
    mov w8, #64
    svc #0

    mov sp, fp
    ldp fp, lr, [sp], #-16
    ret

_start:
    bl main
    ldr w8, =93
    svc #0
    """.strip()
    )


def test_loop():
    ir = Program(
        main=Function(
            "main",
            [
                Loop(
                    [
                        SystemCall(
                            "write",
                            "stdout",
                            String("Hello, World!"),
                        )
                    ]
                )
            ],
        )
    )
    assert open("test_loop.s").read() == aarch64(ir)
