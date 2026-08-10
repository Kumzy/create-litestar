import io
import json
import tarfile
import urllib.error
from pathlib import Path
from typing import Any

import pytest

from create_litestar import __main__ as cli
from create_litestar.helpers import project, registry
from create_litestar.helpers.constants import ARCHIVE_ROOT
from create_litestar.helpers.errors import CreateLitestarError

# mirrors the live templates.json: a top-level "$schema" sibling, an optional
# "featured", and "icon"/"tags" fields the CLI does not use and must ignore.
MANIFEST: dict[str, Any] = {
    "$schema": "./templates.schema.json",
    "templates": [
        {
            "name": "minimal",
            "directory": "minimal",
            "title": "Minimal Litestar",
            "description": "A single route and nothing else.",
            "icon": "i-lucide-globe",
        },
        {
            "name": "api",
            "directory": "api",
            "title": "Litestar API",
            "description": "A REST API organized by domain.",
            "icon": "i-lucide-leaf",
            "featured": True,
            "tags": ["api", "openapi"],
        },
    ],
}


def build_archive(names: list[str]) -> bytes:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
        for name in names:
            payload = f"# {name}".encode()
            info = tarfile.TarInfo(name)
            info.size = len(payload)
            archive.addfile(info, io.BytesIO(payload))
    return buffer.getvalue()


DEFAULT_ARCHIVE = build_archive(
    [
        f"{ARCHIVE_ROOT}/api/README.md",
        f"{ARCHIVE_ROOT}/api/pyproject.toml",
        f"{ARCHIVE_ROOT}/api/src/app/__init__.py",
        f"{ARCHIVE_ROOT}/minimal/README.md",
        f"{ARCHIVE_ROOT}/README.md",
        f"{ARCHIVE_ROOT}/templates.json",
    ]
)


@pytest.fixture(autouse=True)
def fake_registry(monkeypatch: pytest.MonkeyPatch) -> None:
    """Serve the manifest and archive from memory so no test touches the network."""

    def fake_get(url: str) -> bytes:
        if url.endswith("templates.json"):
            return json.dumps(MANIFEST).encode()
        return DEFAULT_ARCHIVE

    monkeypatch.setattr(registry, "get", fake_get)


@pytest.fixture(autouse=True)
def workdir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.chdir(tmp_path)
    return tmp_path


def invoke(*argv: str) -> None:
    cli.run(cli.parse_args(list(argv)))


def test_list_templates(capsys: pytest.CaptureFixture[str]) -> None:
    invoke("--list")

    out = capsys.readouterr().out
    assert "minimal" in out
    assert "api" in out


def test_list_puts_featured_first(capsys: pytest.CaptureFixture[str]) -> None:
    invoke("--list")

    out = capsys.readouterr().out
    assert out.index("api") < out.index("minimal")


def test_scaffold_by_name(workdir: Path) -> None:
    invoke("my-api", "--template", "api")

    target = workdir / "my-api"
    assert (target / "README.md").read_text() == f"# {ARCHIVE_ROOT}/api/README.md"
    assert (target / "pyproject.toml").is_file()
    assert (target / "src" / "app" / "__init__.py").is_file()


def test_scaffold_creates_in_the_current_directory(workdir: Path) -> None:
    invoke("thing", "--template", "minimal")

    assert (workdir / "thing" / "README.md").is_file()
    assert [entry.name for entry in workdir.iterdir()] == ["thing"]


def test_scaffold_excludes_other_templates(workdir: Path) -> None:
    invoke("my-api", "--template", "api")

    target = workdir / "my-api"
    assert not (target / "minimal").exists()
    assert not (target / "templates.json").exists()
    assert not (target / ARCHIVE_ROOT).exists()


def test_project_name_is_slugified(workdir: Path) -> None:
    invoke("My Cool API", "--template", "api")

    assert (workdir / "my-cool-api" / "README.md").is_file()
    assert not (workdir / "My Cool API").exists()


def test_scaffold_prints_next_steps(
    workdir: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    invoke("my-api", "--template", "api")

    out = capsys.readouterr().out
    assert "uv sync" in out
    assert "litestar run" in out
    assert "README.md" in out


def test_unknown_template_suggests_close_match() -> None:
    with pytest.raises(CreateLitestarError, match="api"):
        invoke("out", "--template", "apo")


def test_unknown_template_without_close_match() -> None:
    with pytest.raises(CreateLitestarError, match="--list"):
        invoke("out", "--template", "zzzzzzzz")


def test_existing_non_empty_target_aborts(workdir: Path) -> None:
    target = workdir / "taken"
    target.mkdir()
    (target / "keep.txt").write_text("mine")

    with pytest.raises(CreateLitestarError, match="not empty"):
        invoke("taken", "--template", "api")

    assert (target / "keep.txt").read_text() == "mine"
    assert not (target / "README.md").exists()


def test_existing_empty_target_is_allowed(workdir: Path) -> None:
    (workdir / "empty").mkdir()

    invoke("empty", "--template", "api")

    assert (workdir / "empty" / "README.md").is_file()


def test_path_traversal_member_is_rejected(
    workdir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    malicious = build_archive(
        [f"{ARCHIVE_ROOT}/api/ok.txt", f"{ARCHIVE_ROOT}/api/../../evil.txt"]
    )
    monkeypatch.setattr(
        registry,
        "get",
        lambda url: json.dumps(MANIFEST).encode() if "json" in url else malicious,
    )

    with pytest.raises(CreateLitestarError):
        invoke("out", "--template", "api")

    assert not (workdir / "out").exists()
    assert not (workdir.parent / "evil.txt").exists()


def test_partial_extraction_leaves_no_temporary_files(
    workdir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    malicious = build_archive(
        [f"{ARCHIVE_ROOT}/api/ok.txt", f"{ARCHIVE_ROOT}/api/../../evil.txt"]
    )
    monkeypatch.setattr(
        registry,
        "get",
        lambda url: json.dumps(MANIFEST).encode() if "json" in url else malicious,
    )

    with pytest.raises(CreateLitestarError):
        invoke("out", "--template", "api")

    assert list(workdir.iterdir()) == []


def test_template_without_matching_archive_directory(
    workdir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    empty = build_archive([f"{ARCHIVE_ROOT}/README.md"])
    monkeypatch.setattr(
        registry,
        "get",
        lambda url: json.dumps(MANIFEST).encode() if "json" in url else empty,
    )

    with pytest.raises(CreateLitestarError):
        invoke("out", "--template", "api")

    assert not (workdir / "out").exists()


def test_network_failure_is_friendly(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.undo()  # drop the fake registry so the real urlopen path runs

    def boom(*args: Any, **kwargs: Any) -> None:
        raise urllib.error.URLError("Name or service not known")

    monkeypatch.setattr("urllib.request.urlopen", boom)

    with pytest.raises(CreateLitestarError, match="could not fetch"):
        registry.fetch_templates()


def test_http_error_is_friendly(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.undo()  # drop the fake registry so the real urlopen path runs

    def not_found(*args: Any, **kwargs: Any) -> None:
        raise urllib.error.HTTPError("https://example.com", 404, "Not Found", {}, None)  # type: ignore[arg-type]

    monkeypatch.setattr("urllib.request.urlopen", not_found)

    with pytest.raises(CreateLitestarError, match="404"):
        registry.fetch_templates()


def test_malformed_manifest_is_friendly(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(registry, "get", lambda url: b"<html>not json</html>")

    with pytest.raises(CreateLitestarError, match="could not read"):
        registry.fetch_templates()


def test_main_turns_errors_into_exit_code(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", ["create-litestar", "out", "--template", "nope"])

    with pytest.raises(SystemExit) as excinfo:
        cli.main()

    assert excinfo.value.code == 1


def test_interactive_prompts_drive_the_scaffold(
    workdir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    templates = registry.fetch_templates()
    monkeypatch.setattr(cli, "select_template", lambda _: templates[1])
    monkeypatch.setattr(cli, "ask_project_name", lambda _: "My Cool API")

    invoke()

    assert (
        workdir / "my-cool-api" / "README.md"
    ).read_text() == f"# {ARCHIVE_ROOT}/minimal/README.md"


def test_template_parses_optional_and_unused_fields() -> None:
    """`featured` is optional, and registry fields the CLI does not use (icon, tags) are ignored."""
    by_name = {template.name: template for template in registry.fetch_templates()}

    assert by_name["minimal"].featured is False
    assert by_name["api"].featured is True
    assert not hasattr(by_name["api"], "tags")


def test_registry_entry_missing_required_field(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        registry,
        "get",
        lambda url: json.dumps({"templates": [{"name": "broken"}]}).encode(),
    )

    with pytest.raises(CreateLitestarError, match="directory"):
        registry.fetch_templates()


def test_archive_root_uses_repository_name_not_owner() -> None:
    """GitHub names the tarball folder after the repository, so the owner must not appear in it."""
    assert "/" not in ARCHIVE_ROOT
    assert ARCHIVE_ROOT == "litestar-templates-main"


@pytest.mark.parametrize(
    ("answer", "expected"),
    [
        ("my-app", "my-app"),
        ("My Cool API", "my-cool-api"),
        ("  Spaced  Out  ", "spaced-out"),
        ("under_scored", "under-scored"),
        ("Weird!!Chars??", "weird-chars"),
        ("MiXeD", "mixed"),
    ],
)
def test_slugify(answer: str, expected: str) -> None:
    assert project.slugify(answer) == expected


def test_slugify_rejects_unusable_names() -> None:
    with pytest.raises(CreateLitestarError):
        project.slugify("---")
