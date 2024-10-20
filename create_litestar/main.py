import questionary
from rich.console import Console
import os
import sys
from helpers.validators import NameValidator
from helpers.project import create_project, add_dependencies, copy_project, remove_files, sync_project
from helpers.gitignore import  add_gitignore
from model.project import Project

from commands.logging import logging_choices
from commands.template import template_choices, TemplateEnum
from commands.orm import orm_choices
from commands.object_type import object_type_choices
from commands.web_server import web_server_choices
from commands.openapi import openapi_choices
from commands.plugins import plugin_choices

from helpers.cli import litestar_style, get_qmark
from helpers.constants import DEFAULT_PROJECT_NAME

console = Console()


from pathlib import Path

def get_project_root(marker_file='.git') -> Path:
    current_dir = Path.cwd()
    if (current_dir / marker_file).exists():
        return current_dir
    for parent in current_dir.parents:
        if (parent / marker_file).exists():
            return parent
    raise FileNotFoundError("Project root not found")


def main():
    # To be replaced but quick
    is_debug = any(x in '--debug' for x in sys.argv)
    project_root = get_project_root()
    project = Project()
    console.print()
    console.print("[yellow bold]Litestar - The powerful, lightweight and flexible ASGI framework")
    console.print()

    """Project name"""
    project.project_name = questionary.text(
        message="Project name:",
        qmark=get_qmark(),
        style=litestar_style,
        default=DEFAULT_PROJECT_NAME,
        validate=NameValidator,
    ).ask()

    if project.project_name is None:
        exit(1)

    """Template"""
    selected_template = questionary.select(
        message="Create from a template?",
        qmark=get_qmark(),
        choices=template_choices,
        style=litestar_style
    ).ask()

    if selected_template is None:
        exit(1)

    USE_TEMPLATE = True
    if selected_template == TemplateEnum.NONE:
        USE_TEMPLATE = False

    """Logging"""
    selected_logging = questionary.select(
        message="Add logging?",
        qmark=get_qmark(),
        choices=logging_choices,
        style=litestar_style
    ).skip_if(USE_TEMPLATE).ask()

    if selected_logging is None:
        exit(1)

    project.set_logging(selected_logging)

    """ORM"""
    selected_orm = questionary.select(
        message="Add ORM?",
        qmark=get_qmark(),
        choices=orm_choices,
        style=litestar_style
    ).skip_if(USE_TEMPLATE).ask()

    if selected_orm is None:
        exit(1)

    project.set_orm(selected_orm)

    """Objects"""
    selected_object = questionary.select(
        message="Select object type",
        qmark=get_qmark(),
        choices=object_type_choices,
        style=litestar_style
    ).skip_if(USE_TEMPLATE).ask()

    if selected_object is None:
        exit(1)

    project.set_object_type(selected_object)

    """Web server"""
    selected_web_server = questionary.select(
        message="Add web server?",
        qmark=get_qmark(),
        choices=web_server_choices,
        style=litestar_style
    ).skip_if(USE_TEMPLATE).ask()

    if selected_web_server is None:
        exit(1)

    project.set_web_server(selected_web_server)

    """Test"""
    selected_test = questionary.confirm(
        message="Add pytest for unit tests?",
        qmark=get_qmark(),
        style=litestar_style,
    ).skip_if(USE_TEMPLATE).ask()

    if selected_test is None:
        exit(1)

    project.use_test = bool(selected_test)


    """CORS/CSRF"""
    selected_cors_csrf = questionary.confirm(
        message="Add CORS/CSRF?",
        qmark=get_qmark(),
        style=litestar_style,
    ).skip_if(USE_TEMPLATE).ask()

    if selected_cors_csrf is None:
        exit(1)

    project.use_cors_csrf = bool(selected_cors_csrf)

    """Automatic schema documentation"""
    selected_openapi_schema = questionary.select(
        message="Add automatic schema documentation?",
        qmark=get_qmark(),
        choices=openapi_choices,
        style=litestar_style
    ).skip_if(USE_TEMPLATE).ask()

    if selected_openapi_schema is None:
        exit(1)

    project.set_openapi(selected_openapi_schema)

    """Plugins"""
    selected_plugins = questionary.checkbox(
        message="Add plugins?",
        qmark=get_qmark(),
        choices=plugin_choices,
        style=litestar_style
    ).skip_if(USE_TEMPLATE).ask()

    if selected_plugins is None:
        exit(1)

    print()
    print(f"Scaffolding project in in {project_root.joinpath("output")}")

    new_project_root = Path(get_project_root()).joinpath(project.project_name)
    if is_debug: console.log(str(new_project_root))
    template_path = Path(get_project_root()).joinpath('create_litestar', 'templates', 'basic')
    if is_debug: console.log(str(template_path))

    if is_debug: console.log(project.__dict__)

    # if not os.path.exists(new_project_root):
    #     os.makedirs(new_project_root)
    #
    # os.chdir(new_project_root)

    result = create_project(project.project_name, new_project_root)
    # deps = ["litestar", "advanced-alchemy", "ruff", "pytest", "structlog", "uvicorn"]
    # dependencies = add_dependencies(new_project_root, deps)


    add_gitignore(new_project_root)

    copy_project(template_path=template_path, project_root=new_project_root, data=project)
    sync_project(project_root=new_project_root)
    remove_files(new_project_root)

    console.print()
    console.print("Done. Now run:")
    console.print()
    console.print(f"[yellow bold]    cd {project.project_name}")
    console.print("[yellow bold]    uv run app run")
    console.print()

if __name__ == "__main__":
    main()