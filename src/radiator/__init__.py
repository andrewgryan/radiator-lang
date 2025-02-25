from pydantic import BaseModel
import radiator.lexer
import radiator.parser


class IR(BaseModel):
    ast: radiator.parser.AST

    def to_aarch64(self):
        defs = []
        for fn in self.ast.functions:
            dfn = [f"{fn.signature.identifier}:"]
            if isinstance(fn.block.expression, radiator.parser.Call):
                dfn += [
                    "    stp fp, lr, [sp, #-16]!",
                    "    mov fp, sp",
                    f"    bl {fn.block.expression.identifier}",
                    "    mov sp, fp",
                    "    ldp fp, lr, [sp], #16",
                ]
            else:
                dfn += [f"    mov x0, #{fn.block.expression}"]
            dfn += ["    ret", ""]
            defs += dfn

        if isinstance(self.ast.entry_point, radiator.parser.Call):
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
    tokens = radiator.lexer.lex(code)
    ast = radiator.parser.parse(tokens)
    return IR(ast=ast)
