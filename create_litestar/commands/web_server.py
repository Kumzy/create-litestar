from typing import List, Union
from questionary import Choice, Separator

web_server_choices: List[Union[Choice, Separator, str]]  = [
    Choice(
        title="Granian",
        value=0,
        disabled="Not implemented yet"
    ),
    Choice(
        title="Uvicorn",
        value=1,
        disabled="Not implemented yet"
    ),
    Separator(),
    "None"
]