from enum import StrEnum
from typing import List, Union
from questionary import Choice, Separator


class WebServerEnum(StrEnum):
    GRANIAN = "granian"
    UVICORN = "uvicon"
    NONE = "none"


web_server_choices: List[Union[Choice, Separator, str]] = [
    Choice(
        title="Granian",
        value=WebServerEnum.GRANIAN,
    ),
    Choice(title="Uvicorn", value=WebServerEnum.UVICORN),
    Separator(),
    Choice(title="None", value=WebServerEnum.NONE),
]
