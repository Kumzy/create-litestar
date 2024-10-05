from typing import List, Union
from questionary import Choice, Separator

logging_choices: List[Union[Choice, Separator, str]] = [
    Choice(
        title="Python logging",
        value=0,
        disabled="Not implemented yet"
    ),
    Choice(
        title="Structlog",
        value=1,
        disabled="Not implemented yet"
    ),
    Choice(
        title="Picologging",
        value=2,
        disabled="Not implemented yet"
    ),
    Separator(),
    "None"
]