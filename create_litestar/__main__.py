from pathlib import Path
import sys
import questionary
from rich.console import Console

from create_litestar.helpers.validators import NameValidator
from create_litestar.helpers.project import (
    create_project,
    copy_project,
    remove_files,
    sync_project,
)
from create_litestar.model.project import Project

from create_litestar.commands.logging import logging_choices
from create_litestar.commands.template import template_choices, TemplateEnum
from create_litestar.commands.orm import orm_choices
from create_litestar.commands.object_type import object_type_choices
from create_litestar.commands.web_server import web_server_choices
from create_litestar.commands.openapi import openapi_choices
from create_litestar.commands.plugins import plugin_choices

from create_litestar.helpers.cli import litestar_style, get_qmark
from create_litestar.helpers.constants import DEFAULT_PROJECT_NAME

console = Console()


def main():
    # To be replaced but quick
    is_debug = any(x in "--debug" for x in sys.argv)
    project = Project()
    console.print()
    console.print(
        "[yellow bold]Litestar - The powerful, lightweight and flexible ASGI framework"
    )
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
        style=litestar_style,
    ).ask()

    if selected_template is None:
        exit(1)

    USE_TEMPLATE = True
    if selected_template == TemplateEnum.NONE:
        USE_TEMPLATE = False

    """Logging"""
    selected_logging = (
        questionary.select(
            message="Add logging?",
            qmark=get_qmark(),
            choices=logging_choices,
            style=litestar_style,
        )
        .skip_if(USE_TEMPLATE)
        .ask()
    )

    if selected_logging is None:
        exit(1)

    project.set_logging(selected_logging)

    """ORM"""
    selected_orm = (
        questionary.select(
            message="Add ORM?",
            qmark=get_qmark(),
            choices=orm_choices,
            style=litestar_style,
        )
        .skip_if(USE_TEMPLATE)
        .ask()
    )

    if selected_orm is None:
        exit(1)

    project.set_orm(selected_orm)

    """Objects"""
    selected_object = (
        questionary.select(
            message="Select object type",
            qmark=get_qmark(),
            choices=object_type_choices,
            style=litestar_style,
        )
        .skip_if(USE_TEMPLATE)
        .ask()
    )

    if selected_object is None:
        exit(1)

    project.set_object_type(selected_object)

    """Web server"""
    selected_web_server = (
        questionary.select(
            message="Add web server?",
            qmark=get_qmark(),
            choices=web_server_choices,
            style=litestar_style,
        )
        .skip_if(USE_TEMPLATE)
        .ask()
    )

    if selected_web_server is None:
        exit(1)

    project.set_web_server(selected_web_server)

    """Test"""
    selected_test = (
        questionary.confirm(
            message="Add pytest for unit tests?",
            qmark=get_qmark(),
            style=litestar_style,
        )
        .skip_if(USE_TEMPLATE)
        .ask()
    )

    if selected_test is None:
        exit(1)

    project.use_test = bool(selected_test)

    """CORS/CSRF"""
    selected_cors_csrf = (
        questionary.confirm(
            message="Add CORS/CSRF?",
            qmark=get_qmark(),
            style=litestar_style,
        )
        .skip_if(USE_TEMPLATE)
        .ask()
    )

    if selected_cors_csrf is None:
        exit(1)

    project.use_cors_csrf = bool(selected_cors_csrf)

    """Automatic schema documentation"""
    selected_openapi_schema = (
        questionary.select(
            message="Add automatic schema documentation?",
            qmark=get_qmark(),
            choices=openapi_choices,
            style=litestar_style,
        )
        .skip_if(USE_TEMPLATE)
        .ask()
    )

    if selected_openapi_schema is None:
        exit(1)

    project.set_openapi(selected_openapi_schema)

    """Plugins"""
    selected_plugins = (
        questionary.checkbox(
            message="Add plugins?",
            qmark=get_qmark(),
            choices=plugin_choices,
            style=litestar_style,
        )
        .skip_if(USE_TEMPLATE)
        .ask()
    )

    if selected_plugins is None:
        exit(1)

    new_project_root = Path.cwd().joinpath(project.project_name)

    print()
    print(f"Scaffolding project in in {new_project_root}")

    if is_debug:
        console.log(str(new_project_root))
    template_path = Path(__file__).parent.resolve().joinpath("templates", "basic")
    if is_debug:
        console.log(str(template_path))

    if is_debug:
        console.log(project.__dict__)

    # if not os.path.exists(new_project_root):
    #     os.makedirs(new_project_root)
    #
    # os.chdir(new_project_root)

    result = create_project(project.project_name, new_project_root)
    if not result:
        exit(1)

    copy_project(
        template_path=template_path, project_root=new_project_root, data=project
    )
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
