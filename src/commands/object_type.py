from typing import List
from questionary import Choice

object_type_choices: List[Choice]  = [
    Choice(
        title="Dataclasses",
        value=0,
        disabled="Not implemented yet"
    ),
    Choice(
        title="Pydantic models",
        value=1,
        disabled="Not implemented yet"
    ),
    Choice(
        title="Pydantic dataclasses",
        value=2,
        disabled="Not implemented yet"
    ),
    Choice(
        title="msgspec",
        value=3,
    ),
    Choice(
        title="attrs",
        value=4,
        disabled="Not implemented yet"
    ),
    Choice(
        title="TypedDict",
        value=5,
        disabled="Not implemented yet"
    ),
]