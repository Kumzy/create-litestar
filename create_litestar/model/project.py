from commands.logging import LoggingEnum

class Project:
    project_name: str
    use_logging: bool
    logging: str

    def set_logging(self, logging: str | None):
        if logging and logging  != LoggingEnum.NONE:
            self.use_logging = True
            self.logging = logging
        else:
            self.use_logging = False