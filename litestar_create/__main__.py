import argparse
from pathlib import Path

import questionary
from rich.console import Console
from rich.style import Style
from rich.table import Table

from litestar_create.helpers.cli import get_qmark, litestar_style
from litestar_create.helpers.constants import ARCHIVE_ROOT, LITESTAR_COLOR
from litestar_create.helpers.errors import LitestarCreateError
from litestar_create.helpers.project import ensure_available, extract_template, slugify
from litestar_create.helpers.registry import (
    Template,
    download_archive,
    fetch_templates,
    find_template,
)
from litestar_create.helpers.validators import NameValidator

console = Console()
console_style = Style(color=LITESTAR_COLOR, bold=True)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="litestar-create",
        description="Create a new Litestar project",
    )
    parser.add_argument("name", nargs="?", help="Name of the new project")
    parser.add_argument("-t", "--template", help="Template to scaffold from")
    parser.add_argument(
        "--list",
        action="store_true",
        help="List the available templates and exit",
    )
    return parser.parse_args(argv)


def templates_table(templates: tuple[Template, ...]) -> Table:
    table = Table(title="Litestar templates")
    table.add_column("Name", style="bright_blue", no_wrap=True)
    table.add_column("Description")
    for template in templates:
        table.add_row(template.name, template.description)
    return table


def select_template(templates: tuple[Template, ...]) -> Template:
    answer = questionary.select(
        message="Template:",
        choices=[
            questionary.Choice(title=f"{t.name} - {t.description}", value=t)
            for t in templates
        ],
        qmark=get_qmark(),
        style=litestar_style,
    ).ask()
    if answer is None:
        raise SystemExit(1)
    return answer


def ask_project_name(template: Template) -> str:
    answer = questionary.text(
        message="Project name:",
        qmark=get_qmark(),
        style=litestar_style,
        default=template.name,
        validate=NameValidator,
    ).ask()
    if answer is None:
        raise SystemExit(1)
    return answer


def print_banner() -> None:
    console.print()
    console.print(
        "Litestar - The powerful, lightweight and flexible ASGI framework",
        style=console_style,
    )
    console.print()


def print_next_steps(target: Path) -> None:
    console.print(f"\n[green]Created {target.name}[/]\n")
    console.print(f"  cd {target.name}", style=console_style)
    console.print(
        r"  uv sync  [dim]# or: python -m venv .venv && .venv/bin/pip install -e .[/]",
    )
    console.print("  uv run litestar run --reload")
    console.print(
        f"\n[dim]See {target.name}/README.md for template-specific instructions.[/]",
    )


def run(args: argparse.Namespace) -> None:
    templates = fetch_templates()

    if args.list:
        console.print(templates_table(templates))
        return

    template = (
        find_template(templates, args.template)
        if args.template
        else select_template(templates)
    )
    name = args.name or ask_project_name(template)
    target = Path.cwd() / slugify(name)
    ensure_available(target)
    extract_template(
        download_archive(),
        f"{ARCHIVE_ROOT}/{template.directory}/",
        target,
    )
    print_next_steps(target)


def main() -> None:
    args = parse_args()
    if not args.list:
        print_banner()
    try:
        run(args)
    except LitestarCreateError as e:
        console.print(f"[red]{e}[/]")
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()
