import http.client
import json
import urllib.error
import urllib.request
from collections.abc import Sequence
from dataclasses import dataclass
from difflib import get_close_matches
from typing import Any

from litestar_create.helpers.constants import (
    MANIFEST_URL,
    REQUEST_TIMEOUT,
    TARBALL_URL,
)
from litestar_create.helpers.errors import LitestarCreateError


@dataclass(frozen=True)
class Template:
    name: str
    directory: str
    description: str


def get(url: str) -> bytes:
    if not url.startswith("https://"):
        raise LitestarCreateError(f"refusing to fetch a non-HTTPS url: {url}")
    try:
        with urllib.request.urlopen(url, timeout=REQUEST_TIMEOUT) as response:
            return bytes(response.read())
    except urllib.error.HTTPError as e:
        raise LitestarCreateError(
            f"could not fetch {url}: the server responded with {e.code} {e.reason}"
        ) from e
    except (urllib.error.URLError, http.client.HTTPException, OSError) as e:
        raise LitestarCreateError(
            f"could not fetch {url}: {e}. Check your network connection"
        ) from e


def parse_template(entry: dict[str, Any]) -> Template:
    if not isinstance(entry, dict):
        raise LitestarCreateError(
            f"template registry entry is not an object: {entry!r}"
        )
    try:
        return Template(
            name=entry["name"],
            directory=entry["directory"],
            description=entry.get("description", ""),
        )
    except KeyError as e:
        raise LitestarCreateError(
            f"template registry entry is missing the {e} field"
        ) from e


def fetch_templates() -> tuple[Template, ...]:
    payload = get(MANIFEST_URL)
    try:
        entries = json.loads(payload)["templates"]
    except (json.JSONDecodeError, UnicodeDecodeError, KeyError, TypeError) as e:
        raise LitestarCreateError(
            f"could not read the template registry at {MANIFEST_URL}: {e}"
        ) from e
    # Preserve the registry's own ordering.
    templates = tuple(parse_template(entry) for entry in entries)
    if not templates:
        raise LitestarCreateError(f"the template registry at {MANIFEST_URL} is empty")
    return templates


def find_template(templates: Sequence[Template], name: str) -> Template:
    for template in templates:
        if template.name == name:
            return template
    matches = get_close_matches(
        name, [template.name for template in templates], n=3, cutoff=0.5
    )
    hint = f" Did you mean: {', '.join(matches)}?" if matches else ""
    raise LitestarCreateError(
        f"unknown template {name!r}.{hint} Run 'litestar-create --list' to see every template"
    )


def download_archive() -> bytes:
    return get(TARBALL_URL)
