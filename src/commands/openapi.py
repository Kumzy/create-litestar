from typing import List, Union
from questionary import Choice, Separator

openapi_choices: List[Union[Choice, Separator, str]]  = [
    Choice(
        title="Scalar",
        value=0,
        disabled="Not implemented yet"
    ),
    Choice(
        title="RapiDoc",
        value=1,
        disabled="Not implemented yet"
    ),
    Choice(
        title="Swagger-UI",
        value=2,
        disabled="Not implemented yet"
    ),
    Choice(
        title="Spotlight Elements",
        value=3,
        disabled="Not implemented yet"
    ),
    Choice(
        title="Redoc",
        value=4,
        disabled="Not implemented yet"
    ),
    Separator(),
    "None"
]