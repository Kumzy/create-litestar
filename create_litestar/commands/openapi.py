from enum import StrEnum
from typing import List, Union
from questionary import Choice, Separator


class OpenApiEnum(StrEnum):
    SCALAR = "scalar"
    RAPIDOC = "rapid_doc"
    SWAGGERUI = "swagger_ui"
    SPOTLIGHTELEMENTS = "spotlight_elements"
    REDOC = "redoc"
    NONE = "none"


openapi_choices: List[Union[Choice, Separator, str]] = [
    Choice(title="Scalar", value=OpenApiEnum.SCALAR),
    Choice(title="RapiDoc", value=OpenApiEnum.RAPIDOC, disabled="Not implemented yet"),
    Choice(
        title="Swagger-UI", value=OpenApiEnum.SWAGGERUI, disabled="Not implemented yet"
    ),
    Choice(
        title="Spotlight Elements",
        value=OpenApiEnum.SPOTLIGHTELEMENTS,
        disabled="Not implemented yet",
    ),
    Choice(title="Redoc", value=OpenApiEnum.REDOC, disabled="Not implemented yet"),
    Separator(),
    Choice(title="None", value=OpenApiEnum.NONE),
]
