from typing import List, Union
from questionary import Choice, Separator

template_choices: List[Union[Choice, Separator, str]]  = [
    Choice(
        title="Litestar fullstack (react)",
        value=0,
        disabled="Not implemented yet"
    ),
    Choice(
        title="Litestar + htmx",
        value=1,
        disabled="Not implemented yet"
    ),
    Choice(
        title="Litestar fullstack (inertia)",
        value=2,
        disabled="Not implemented yet"
    ),
    Separator(),
    "None"
]