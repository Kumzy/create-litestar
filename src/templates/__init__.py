from enum import Enum

class TemplateType(Enum):
    LOCAL = 1
    REMOTE = 2


class LitestarTemplate():
    template_type: TemplateType = 1
