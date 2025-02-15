class IR:
    def to_aarch64(self):
        lines = [
            ".text",
            ".global _start",
            "_start:",
            "    ldr w8, =93",
            "    ldr x0, =0",
            "    svc #0",
        ]
        return "\n".join(lines) + "\n"



def compile(code: str) -> IR:
    return IR()
