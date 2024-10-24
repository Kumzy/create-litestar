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
    Choice(title="RapiDoc", value=OpenApiEnum.RAPIDOC),
    Choice(title="Swagger-UI", value=OpenApiEnum.SWAGGERUI),
    Choice(title="Spotlight Elements", value=OpenApiEnum.SPOTLIGHTELEMENTS),
    Choice(title="Redoc", value=OpenApiEnum.REDOC),
    Separator(),
    Choice(title="None", value=OpenApiEnum.NONE),
]
