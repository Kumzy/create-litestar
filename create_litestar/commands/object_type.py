from enum import StrEnum
from typing import List
from questionary import Choice


class ObjectTypeEnum(StrEnum):
    DATACLASSES = "dataclasses"
    PYDANTICMODELS = "pydantic_models"
    PYDANTICDATACLASSES = "pydantic_dataclasses"
    MSGSPEC = "msgspec"
    ATTRS = "attrs"
    TYPEDDICT = "typed_dict"
    NONE = "none"


object_type_choices: List[Choice] = [
    Choice(
        title="Dataclasses",
        value=ObjectTypeEnum.DATACLASSES,
        disabled="Not implemented yet",
    ),
    Choice(
        title="Pydantic models",
        value=ObjectTypeEnum.PYDANTICMODELS,
        disabled="Not implemented yet",
    ),
    Choice(
        title="Pydantic dataclasses",
        value=ObjectTypeEnum.PYDANTICDATACLASSES,
        disabled="Not implemented yet",
    ),
    Choice(
        title="msgspec",
        value=ObjectTypeEnum.MSGSPEC,
    ),
    Choice(title="attrs", value=ObjectTypeEnum.ATTRS, disabled="Not implemented yet"),
    Choice(
        title="TypedDict",
        value=ObjectTypeEnum.TYPEDDICT,
        disabled="Not implemented yet",
    ),
]
