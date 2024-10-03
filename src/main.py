import questionary
from questionary import Separator
from questionary import Style
from rich.console import Console

console = Console()

custom_style_dope = Style(
    [
        ("separator", "fg:#6C6C6C"),
        ("qmark", "fg:#FF9D00 bold"),
        ("question", ""),
        ("selected", "fg:#5F819D"),
        ("pointer", "fg:#FF9D00 bold"),
    ]
)

def main():

    print("Litestar - The powerful, lightweight and flexible ASGI framework")

    """Project name"""
    project_name = questionary.text("Project name:").ask()

    """Logging"""
    loggings = ["Python logging", "StructLog", "Picologging", Separator(), "None"]

    selected_logging = questionary.select(
        message="Add logging?",
        qmark="✔️",
        choices=loggings,
        style=custom_style_dope
    ).ask()

    """ORM"""
    orms = ["SqlAlchemy", "Picollo ORM",Separator(), "None"]

    selected_orm = questionary.select(
        "Add ORM?",
        choices=orms
    ).ask()

    """Objects"""
    objects = ["Dataclasses", "Pydantic models", "Pydantic dataclasses", "msgspec"]

    selected_object = questionary.select(
        "Select object type",
        choices=objects
    ).ask()

    """Web server"""
    web_servers = ["Granian", "Uvicorn", Separator(), "None"]

    selected_web_server = questionary.select(
        "Add web server?",
        choices=web_servers
    ).ask()


if __name__ == "__main__":
    main()