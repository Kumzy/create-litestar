from questionary import Style

litestar_style = Style(
    [
        ("separator", "fg:#6C6C6C"),
        ("qmark", "fg:#FF9D00 bold"),
        ("question", ""),
        ("selected", "fg:#5F819D"),
        ("pointer", "fg:#FF9D00 bold"),
        ("disabled", "fg:#858585 italic"),
    ]
)


def get_qmark() -> str:
    return "✔"
