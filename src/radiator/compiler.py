# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pydantic",
#     "typer",
# ]
# ///
import radiator
import typer
import subprocess
from typing import Annotated

app = typer.Typer()


@app.command()
def main(script: str, out: Annotated[str, typer.Option("-o", "--out")] = "main") -> None:
    with open(script, "r") as stream:
        text = stream.read()
        code = radiator.compile(text).to_aarch64()
        if out:
            with open(out, "w") as stream:
                stream.write(code)
        else:
            print(code)

        # Compile assembly to executable
        status = subprocess.call(["as", "-o", "main.o", out])
        if status == 0:
            status = subprocess.call(["ld", "-o", "main", "main.o"])
