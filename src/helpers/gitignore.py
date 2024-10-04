from pathlib import Path
import httpx
import os
from .constants import PYTHON_GITIGNORE_URL

def add_gitignore(project_root: Path):
    """Download python gitignore"""
    r = httpx.get(PYTHON_GITIGNORE_URL, timeout=20)
    with open(f'{project_root}/.gitignore', 'wb') as f:
        f.write(r.content)

    if not os.path.exists(os.path.join(project_root, ".gitignore")):
        raise Exception(f"Error installing gitignore")