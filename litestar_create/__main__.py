import argparse
from pathlib import Path

import questionary

from litestar_create.helpers.cli import (
    DIM,
    GOLD,
    GREEN,
    RED,
    echo,
    get_qmark,
    litestar_style,
)
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


def print_templates(templates: tuple[Template, ...]) -> None:
    width = max(len(template.name) for template in templates)
    echo((GOLD, "Litestar templates"))
    echo()
    for template in templates:
        echo(
            (f"fg:{LITESTAR_COLOR}", f"  {template.name:<{width}}  "),
            ("", template.description),
        )


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
    echo()
    echo((GOLD, "Litestar - The powerful, lightweight and flexible ASGI framework"))
    echo()


def print_next_steps(target: Path) -> None:
    echo()
    echo((GREEN, f"Created {target.name}"))
    echo()
    echo((GOLD, f"  cd {target.name}"))
    echo(
        ("", "  uv sync  "),
        (DIM, "# or: python -m venv .venv && .venv/bin/pip install -e ."),
    )
    echo(("", "  uv run litestar run --reload"))
    echo()
    echo((DIM, f"See {target.name}/README.md for template-specific instructions."))


def run(args: argparse.Namespace) -> None:
    templates = fetch_templates()

    if args.list:
        print_templates(templates)
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
        echo((RED, str(e)))
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()
