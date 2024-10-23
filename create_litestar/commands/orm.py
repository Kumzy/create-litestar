from enum import StrEnum
from typing import List, Union
from questionary import Choice, Separator


class OrmEnum(StrEnum):
    SQLALCHEMY = "sqlalchemy"
    PICOLLO = "picollo"
    TORTOISE = "tortoise"
    NONE = "none"


orm_choices: List[Union[Choice, Separator, str]] = [
    Choice(
        title="SQLAlchemy + alembic",
        value=OrmEnum.SQLALCHEMY,
    ),
    Choice(title="Picollo ORM", value=OrmEnum.PICOLLO, disabled="Not implemented yet"),
    Choice(title="Tortoise", value=OrmEnum.TORTOISE, disabled="Not implemented yet"),
    Separator(),
    Choice(title="None", value=OrmEnum.NONE),
]
