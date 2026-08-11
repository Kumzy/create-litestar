import sys

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from questionary import Style

from litestar_create.helpers.constants import LITESTAR_COLOR

GOLD = f"fg:{LITESTAR_COLOR} bold"
GREEN = "fg:ansigreen"
RED = "fg:ansired"
DIM = "fg:#808080"

litestar_style = Style(
    [
        ("separator", "fg:#6C6C6C"),
        ("qmark", f"fg:{LITESTAR_COLOR} bold"),
        ("question", ""),
        ("selected", f"fg:{LITESTAR_COLOR}"),
        ("pointer", f"fg:{LITESTAR_COLOR} bold"),
        ("disabled", "fg:#858585 italic"),
    ],
)


def echo(*fragments: tuple[str, str]) -> None:
    """Print (style, text) fragments, styled via prompt_toolkit on a terminal.

    Falls back to plain print when stdout is not a TTY (pipes, redirects,
    test capture), which also keeps piped output free of escape codes.
    """
    if sys.stdout.isatty():
        print_formatted_text(FormattedText(list(fragments)))
    else:
        print("".join(text for _, text in fragments))


def get_qmark() -> str:
    return "✔"
