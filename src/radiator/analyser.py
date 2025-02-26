from pydantic import BaseModel


class Error(BaseModel):
    msg: str


class Result(BaseModel):
    errors: list[Error]


def analyse(ast):
    errors = []
    for fn in ast.functions:
        if not isinstance(fn.block.expression, int):
            msg = f"undefined symbol '{fn.block.expression}'"
            errors.append(Error(msg=msg))
    return Result(errors=errors)
