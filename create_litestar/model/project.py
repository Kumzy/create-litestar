from create_litestar.commands.logging import LoggingEnum
from create_litestar.commands.orm import OrmEnum
from create_litestar.commands.openapi import OpenApiEnum

from create_litestar.helpers.constants import DEFAULT_PROJECT_DESCRIPTION

class Project:
    project_name: str
    project_description: str = DEFAULT_PROJECT_DESCRIPTION
    """Logging"""
    use_logging: bool
    logging: str
    """ORM"""
    use_orm: bool
    orm: str
    """OpenAPI"""
    use_openapi: bool
    openapi: str

    def set_logging(self, logging: LoggingEnum | None):
        if logging and logging  != LoggingEnum.NONE:
            self.use_logging = True
            self.logging = logging.value
        else:
            self.use_logging = False

    def set_orm(self, orm: OrmEnum | None):
        if orm and orm  != OrmEnum.NONE:
            self.use_orm = True
            self.orm = orm.value
        else:
            self.use_orm = False

    def set_openapi(self, openapi: OpenApiEnum | None):
        if openapi and openapi  != OpenApiEnum.NONE:
            self.use_openapi = True
            self.openapi = openapi.value
        else:
            self.use_openapi = False