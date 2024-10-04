import questionary
from questionary import Separator
from questionary import Style
from rich.console import Console
import os
from helpers.validators import NameValidator
from helpers.project import create_project, add_dependencies
from helpers.gitignore import  add_gitignore
console = Console()

litestar_style = Style(
    [
        ("separator", "fg:#6C6C6C"),
        ("qmark", "fg:#FF9D00 bold"),
        ("question", ""),
        ("selected", "fg:#5F819D"),
        ("pointer", "fg:#FF9D00 bold"),
    ]
)

from pathlib import Path

def find_project_root(marker_file='.git'):
    current_dir = Path.cwd()
    if (current_dir / marker_file).exists():
        return current_dir
    for parent in current_dir.parents:
        if (parent / marker_file).exists():
            return parent
    raise FileNotFoundError("Project root not found")



def main():

    project_root = find_project_root()
    print(project_root)
    print("Litestar - The powerful, lightweight and flexible ASGI framework")

    """Project name"""
    project_name = questionary.text(
        message="Project name:",
        qmark="✔",
        style=litestar_style,
        default="litestar-project",
        validate=NameValidator,
    ).ask()

    if project_name is None:
        exit(1)

    """Template"""
    templates = ["Litestar fullstack (react)", "Litestar + htmx", "Litestar fullstack (inertia)", Separator(), "None"]

    selected_template = questionary.select(
        message="Create from a template?",
        qmark="✔",
        choices=templates,
        style=litestar_style
    ).ask()

    USE_TEMPLATE = True
    if selected_template == "None":
        USE_TEMPLATE = False

    """Logging"""
    loggings = ["Python logging", "StructLog", "Picologging", Separator(), "None"]

    selected_logging = questionary.select(
        message="Add logging?",
        qmark="✔",
        choices=loggings,
        style=litestar_style
    ).skip_if(USE_TEMPLATE).ask()

    """ORM"""
    orms = ["SqlAlchemy", "Picollo ORM", "Tortoise", Separator(), "None"]

    selected_orm = questionary.select(
        message="Add ORM?",
        choices=orms,
        style=litestar_style
    ).skip_if(USE_TEMPLATE).ask()

    """Objects"""
    objects = ["Dataclasses", "Pydantic models", "Pydantic dataclasses", "msgspec", "attrs", "TypedDict"]

    selected_object = questionary.select(
        message="Select object type",
        choices=objects,
        style=litestar_style
    ).skip_if(USE_TEMPLATE).ask()

    """Web server"""
    web_servers = ["Granian", "Uvicorn", Separator(), "None"]

    selected_web_server = questionary.select(
        message="Add web server?",
        choices=web_servers,
        style=litestar_style
    ).skip_if(USE_TEMPLATE).ask()

    """Test"""
    selected_test = questionary.confirm(
        message="Add pytest for unit tests?",
        style=litestar_style,
    ).skip_if(USE_TEMPLATE).ask()

    """Automatic schema documentation"""
    openapi_schemas = [
        "Scalar",
        "RapiDoc",
        "Swagger-UI",
        "Spotlight Elements",
        "Redoc",
        Separator(),
        "None"
    ]

    selected_openapi_schema = questionary.select(
        message="Add automatic schema documentation?",
        choices=openapi_schemas,
        style=litestar_style
    ).skip_if(USE_TEMPLATE).ask()

    """Plugins"""
    plugins = [
        "SAQ",
    ]

    selected_plugins = questionary.checkbox(
        message="Add plugins?",
        choices=plugins,
        style=litestar_style
    ).skip_if(USE_TEMPLATE).ask()

    print(f"Project generation in {project_root}/output")
    # print(f"Project generation in {project_root}/{project_name}")

    new_project_root = f'{project_root}/output'
    if not os.path.exists(new_project_root):
        os.makedirs(new_project_root)

    os.chdir(new_project_root)
    result = create_project(project_name, new_project_root)
    deps = ["litestar", "advanced-alchemy", "ruff", "pytest"]
    dependencies = add_dependencies(new_project_root, deps)

    add_gitignore(new_project_root)

if __name__ == "__main__":
    main()