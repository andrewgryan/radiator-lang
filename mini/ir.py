from dataclasses import dataclass, field
from textwrap import dedent


@dataclass
class String:
    text: str
    identifier: str = None


@dataclass
class SystemCall:
    method: str = "write"
    fd: int = 0
    string: String = None


@dataclass
class Loop:
    statements: list[SystemCall] = field(
        default_factory=list
    )


@dataclass
class Function:
    identifier: str
    statements: list[SystemCall] = field(
        default_factory=list
    )


@dataclass
class Program:
    main: Function

    @property
    def data(self):
        items = []
        for statement in self.main.statements:
            if isinstance(statement, String):
                items.append(statement)
            elif isinstance(statement, Loop):
                items += [
                    st.string
                    for st in statement.statements
                ]

        return items


def x86_64(program: Program) -> str:
    return ""


def aarch64(program: Program) -> str:
    return f"""
{aarch64_data_section(program)}

.text
.global _start

{aarch64_function(program.main)}

_start:
    bl main
    ldr w8, =93
    svc #0
    """.strip()


def aarch64_data_section(program: Program) -> str:
    data_section = ""
    if program.data:
        data_section = "\n".join(
            [".data"]
            + [
                aarch64_data(item)
                for item in program.data
            ]
        )
    return data_section


def aarch64_function(fn: Function):
    return f"""
{fn.identifier}:
    stp fp, lr, [sp, #-16]!
    mov fp, sp

    {aarch64_statements(fn.statements)}

    mov sp, fp
    ldp fp, lr, [sp], #-16
    ret
    """.strip()


def aarch64_statements(statements):
    blocks = []
    for statement in statements:
        if isinstance(statement, SystemCall):
            blocks.append(aarch64_system_call(statement))
        elif isinstance(statement, Loop):
            blocks.append(aarch64_loop(statement))
    return "\n".join(blocks)


def aarch64_loop(loop: Loop):
    return f"""
0:
    {aarch64_statements(loop.statements)}
    ba 0
    """.strip()


def aarch64_system_call(call: SystemCall):
    return f"""
    mov x0, #1
    ldr x1, ={call.string.identifier}
    ldr x2, ={call.string.identifier}_len
    mov w8, #64
    svc #0
    """.strip()


def aarch64_data(s: String):
    return f"""
{s.identifier}:
    .ascii "{s.text}"
{s.identifier}_len = . - {s.identifier}
    """.strip()
