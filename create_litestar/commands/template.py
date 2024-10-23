from enum import StrEnum
from typing import List, Union
from questionary import Choice, Separator


class TemplateEnum(StrEnum):
    FULLSTACKREACT = "react"
    FULLSTACKHTMX = "htmx"
    INERTIA = "inertia"
    NONE = "none"


template_choices: List[Union[Choice, Separator, str]] = [
    Choice(
        title="Litestar fullstack (react)",
        value=TemplateEnum.FULLSTACKREACT,
        disabled="Not implemented yet",
    ),
    Choice(
        title="Litestar + htmx",
        value=TemplateEnum.FULLSTACKHTMX,
        disabled="Not implemented yet",
    ),
    Choice(
        title="Litestar fullstack (inertia)",
        value=TemplateEnum.INERTIA,
        disabled="Not implemented yet",
    ),
    Separator(),
    Choice(title="None", value=TemplateEnum.NONE),
]
