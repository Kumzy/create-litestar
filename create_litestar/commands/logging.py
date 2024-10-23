from enum import StrEnum
from typing import List, Union
from questionary import Choice, Separator


class LoggingEnum(StrEnum):
    PYTHON_LOGGING = "python_logging"
    STRUCTLOG = "structlog"
    PICOLOGGING = "picologging"
    NONE = "none"


logging_choices: List[Union[Choice, Separator]] = [
    Choice(
        title="Python logging",
        value=LoggingEnum.PYTHON_LOGGING,
        disabled="Not implemented yet",
    ),
    Choice(title="Structlog", value=LoggingEnum.STRUCTLOG),
    Choice(
        title="Picologging",
        value=LoggingEnum.PICOLOGGING,
        disabled="Not implemented yet",
    ),
    Separator(),
    Choice(title="None", value=LoggingEnum.NONE),
]
