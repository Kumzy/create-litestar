import io
import re
import shutil
import tarfile
import tempfile
from pathlib import Path

from create_litestar.helpers.errors import CreateLitestarError


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9.-]+", "-", value.strip().lower()).strip("-.")
    if not slug:
        raise CreateLitestarError(f"{value!r} cannot be used as a project name")
    return slug


def ensure_available(target: Path) -> None:
    if not target.exists():
        return
    if target.is_file() or any(target.iterdir()):
        raise CreateLitestarError(f"{target} already exists and is not empty")


def strip_prefix(archive: tarfile.TarFile, prefix: str) -> list[tarfile.TarInfo]:
    members = []
    for member in archive.getmembers():
        if not member.name.startswith(prefix):
            continue
        member.name = member.name[len(prefix) :]
        if member.name:
            members.append(member)
    return members


def move_into(source: Path, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for entry in source.iterdir():
        shutil.move(str(entry), str(target / entry.name))


def extract_template(payload: bytes, prefix: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(dir=target.parent))
    try:
        with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as archive:
            members = strip_prefix(archive, prefix)
            if not members:
                raise CreateLitestarError(
                    f"the template archive contains no files under {prefix!r}"
                )
            archive.extractall(path=staging, members=members, filter="data")
        move_into(staging, target)
    except tarfile.TarError as e:
        raise CreateLitestarError(f"could not extract the template archive: {e}") from e
    finally:
        shutil.rmtree(staging, ignore_errors=True)
