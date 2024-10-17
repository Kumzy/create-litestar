import questionary
from rich.console import Console
import os
import sys
from helpers.validators import NameValidator
from helpers.project import create_project, add_dependencies, copy_project, remove_files
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

    if selected_orm is None:
        exit(1)

    """Web server"""
    selected_web_server = questionary.select(
        message="Add web server?",
        qmark=get_qmark(),
        choices=web_server_choices,
        style=litestar_style
    ).skip_if(USE_TEMPLATE).ask()

    if selected_web_server is None:
        exit(1)

    """Test"""
    selected_test = questionary.confirm(
        message="Add pytest for unit tests?",
        style=litestar_style,
    ).skip_if(USE_TEMPLATE).ask()

    if selected_test is None:
        exit(1)

    """Automatic schema documentation"""
    selected_openapi_schema = questionary.select(
        message="Add automatic schema documentation?",
        choices=openapi_choices,
        style=litestar_style
    ).skip_if(USE_TEMPLATE).ask()

    if selected_openapi_schema is None:
        exit(1)

    project.set_openapi(selected_openapi_schema)

    """Plugins"""
    selected_plugins = questionary.checkbox(
        message="Add plugins?",
        choices=plugin_choices,
        style=litestar_style
    ).skip_if(USE_TEMPLATE).ask()

    if selected_plugins is None:
        exit(1)

    print(f"Project generation in {project_root}/output")
    # print(f"Project generation in {project_root}/{project_name}")

    new_project_root = Path(get_project_root()).joinpath('output')
    if is_debug: console.log(str(new_project_root))
    template_path = Path(get_project_root()).joinpath('create_litestar', 'templates', 'basic')
    if is_debug: console.log(str(template_path))

    if is_debug: console.log(project.__dict__)

    if not os.path.exists(new_project_root):
        os.makedirs(new_project_root)

    os.chdir(new_project_root)
    result = create_project(project.project_name, new_project_root)
    deps = ["litestar", "advanced-alchemy", "ruff", "pytest", "structlog", "uvicorn"]
    dependencies = add_dependencies(new_project_root, deps)

    add_gitignore(new_project_root)

    copy_project(template_path=template_path, project_root=new_project_root, data=project)
    remove_files(new_project_root)

if __name__ == "__main__":
    main()