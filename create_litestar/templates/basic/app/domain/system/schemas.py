import msgspec


class SystemInfo(msgspec.Struct):
    """Instance app"""

    name: str
