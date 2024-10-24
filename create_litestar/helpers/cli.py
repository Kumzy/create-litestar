from questionary import Style
from create_litestar.helpers.constants import LITESTAR_COLOR

litestar_style = Style(
    [
        ("separator", "fg:#6C6C6C"),
        ("qmark", f"fg:{LITESTAR_COLOR} bold"),
        ("question", ""),
        ("selected", f"fg:{LITESTAR_COLOR}"),
        ("pointer", f"fg:{LITESTAR_COLOR} bold"),
        ("disabled", "fg:#858585 italic"),
    ]
)


def get_qmark() -> str:
    return "✔"
