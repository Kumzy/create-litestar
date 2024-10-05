from typing import List, Union
from questionary import Choice, Separator

orm_choices: List[Union[Choice, Separator, str]]  = [
    Choice(
        title="Litestar fullstack (react)",
        value=0,
        disabled="Not implemented yet"
    ),
    Choice(
        title="Picollo ORM",
        value=1,
        disabled="Not implemented yet"
    ),
    Choice(
        title="Tortoise",
        value=2,
        disabled="Not implemented yet"
    ),
    Separator(),
    "None"
]