from pydantic import BaseModel
from typing import Annotated, Union
from typing_extensions import TypeAliasType

Expression = TypeAliasType(
    "Expression", Annotated[list[Union[int, "Expression"]], "Description"]
)


class Model(BaseModel):
    expression: Expression
