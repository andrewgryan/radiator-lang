import re
from pydantic import BaseModel
import radiator.compiler


class IR(BaseModel):
    ast: radiator.compiler.AST

    def to_aarch64(self):
        defs = []
        for fn in self.ast.functions:
            dfn = [f"{fn.identifier}:"]
            if isinstance(fn.return_value, radiator.compiler.Call):
                dfn += [
                    "    stp fp, lr, [sp, #-16]!",
                    "    mov fp, sp",
                    f"    bl {fn.return_value.identifier}",
                    "    mov sp, fp",
                    "    ldp fp, lr, [sp], #16",
                ]
            else:
                dfn += [f"    mov x0, #{fn.return_value}"]
            dfn += ["    ret", ""]
            defs += dfn

        if isinstance(self.ast.entry_point, radiator.compiler.Call):
            entry = [f"    bl {self.ast.entry_point.identifier}"]
        else:
            entry = ["   ldr x0, =0"]

        lines = [
            ".text",
            ".global _start",
            *defs,
            "_start:",
            *entry,
            "    ldr w8, =93",
            "    svc #0",
        ]
        return "\n".join(lines) + "\n"


def compile(code: str) -> IR:
    tokens = radiator.compiler.lex(code)
    ast = radiator.compiler.parse(tokens)
    return IR(ast=ast)
