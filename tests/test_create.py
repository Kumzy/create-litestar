import io
import json
import tarfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from litestar_create import __main__ as cli
from litestar_create.helpers import project, registry
from litestar_create.helpers.constants import ARCHIVE_ROOT
from litestar_create.helpers.errors import LitestarCreateError

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
    ],
)


# The genuine fetcher, captured before any fixture patches it.
REAL_GET = registry.get

ServeFn = Callable[..., None]


@pytest.fixture(autouse=True)
def serve(monkeypatch: pytest.MonkeyPatch) -> ServeFn:
    """Serve the manifest and archive from memory so no test touches the network.

    Applied everywhere with the default payloads; a test re-invokes it to serve
    variants: serve(manifest=...), serve(archive=...).
    """

    def _serve(
        manifest: dict[str, Any] | bytes = MANIFEST,
        archive: bytes = DEFAULT_ARCHIVE,
    ) -> None:
        payload = (
            manifest if isinstance(manifest, bytes) else json.dumps(manifest).encode()
        )
        monkeypatch.setattr(
            registry,
            "get",
            lambda url: payload if url.endswith("templates.json") else archive,
        )

    _serve()
    return _serve


@pytest.fixture
def real_get(monkeypatch: pytest.MonkeyPatch) -> None:
    """Precisely undo the serve fixture: restore the real registry.get."""
    monkeypatch.setattr(registry, "get", REAL_GET)


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
    workdir: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    invoke("my-api", "--template", "api")

    out = capsys.readouterr().out
    assert "uv sync" in out
    assert "litestar run" in out
    assert "README.md" in out


def test_unknown_template_suggests_close_match() -> None:
    with pytest.raises(LitestarCreateError, match="api"):
        invoke("out", "--template", "apo")


def test_unknown_template_without_close_match() -> None:
    with pytest.raises(LitestarCreateError, match="--list"):
        invoke("out", "--template", "zzzzzzzz")


def test_existing_non_empty_target_aborts(workdir: Path) -> None:
    target = workdir / "taken"
    target.mkdir()
    (target / "keep.txt").write_text("mine")

    with pytest.raises(LitestarCreateError, match="not empty"):
        invoke("taken", "--template", "api")

    assert (target / "keep.txt").read_text() == "mine"
    assert not (target / "README.md").exists()


def test_existing_empty_target_is_allowed(workdir: Path) -> None:
    (workdir / "empty").mkdir()

    invoke("empty", "--template", "api")

    assert (workdir / "empty" / "README.md").is_file()


def test_path_traversal_member_is_rejected(workdir: Path, serve: ServeFn) -> None:
    serve(
        archive=build_archive(
            [f"{ARCHIVE_ROOT}/api/ok.txt", f"{ARCHIVE_ROOT}/api/../../evil.txt"],
        )
    )

    with pytest.raises(LitestarCreateError):
        invoke("out", "--template", "api")

    assert not (workdir / "out").exists()
    assert not (workdir.parent / "evil.txt").exists()


def test_partial_extraction_leaves_no_temporary_files(
    workdir: Path,
    serve: ServeFn,
) -> None:
    serve(
        archive=build_archive(
            [f"{ARCHIVE_ROOT}/api/ok.txt", f"{ARCHIVE_ROOT}/api/../../evil.txt"],
        )
    )

    with pytest.raises(LitestarCreateError):
        invoke("out", "--template", "api")

    assert list(workdir.iterdir()) == []


def test_template_without_matching_archive_directory(
    workdir: Path,
    serve: ServeFn,
) -> None:
    serve(archive=build_archive([f"{ARCHIVE_ROOT}/README.md"]))

    with pytest.raises(LitestarCreateError):
        invoke("out", "--template", "api")

    assert not (workdir / "out").exists()


def test_malformed_manifest_is_friendly(serve: ServeFn) -> None:
    serve(manifest=b"<html>not json</html>")

    with pytest.raises(LitestarCreateError, match="could not read"):
        registry.fetch_templates()


def test_main_turns_errors_into_exit_code(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", ["litestar-create", "out", "--template", "nope"])

    with pytest.raises(SystemExit) as excinfo:
        cli.main()

    assert excinfo.value.code == 1


def test_interactive_prompts_drive_the_scaffold(
    workdir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    selected = registry.fetch_templates()[0]
    monkeypatch.setattr(cli, "select_template", lambda _: selected)
    monkeypatch.setattr(cli, "ask_project_name", lambda _: "My Cool API")

    invoke()

    assert (
        workdir / "my-cool-api" / "README.md"
    ).read_text() == f"# {ARCHIVE_ROOT}/{selected.directory}/README.md"


def test_registry_entry_missing_required_field(serve: ServeFn) -> None:
    serve(manifest={"templates": [{"name": "broken"}]})

    with pytest.raises(LitestarCreateError, match="directory"):
        registry.fetch_templates()


@pytest.mark.parametrize(
    ("answer", "expected"),
    [
        ("my-app", "my-app"),
        ("My Cool API", "my-cool-api"),
        ("Weird!!Chars??", "weird-chars"),
    ],
)
def test_slugify(answer: str, expected: str) -> None:
    assert project.slugify(answer) == expected


def test_slugify_rejects_unusable_names() -> None:
    with pytest.raises(LitestarCreateError):
        project.slugify("---")


class CancelledPrompt:
    """Mimics questionary returning None, as it does when the user hits Ctrl-C."""

    def ask(self) -> None:
        return None


def test_cancelling_the_template_prompt_exits_cleanly(
    workdir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("sys.stdin.isatty", lambda: True)  # get past the TTY guard
    monkeypatch.setattr(
        cli.questionary, "select", lambda *args, **kwargs: CancelledPrompt()
    )

    with pytest.raises(SystemExit) as excinfo:
        invoke()

    assert excinfo.value.code == 1
    assert not any(workdir.iterdir())


def test_non_https_urls_are_refused(real_get: None) -> None:
    with pytest.raises(LitestarCreateError, match="non-HTTPS"):
        registry.get("http://raw.githubusercontent.com/templates.json")


def test_empty_registry_is_an_error(serve: ServeFn) -> None:
    serve(manifest={"templates": []})

    with pytest.raises(LitestarCreateError, match="empty"):
        registry.fetch_templates()
