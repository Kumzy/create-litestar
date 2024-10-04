import os
import subprocess
from pathlib import Path

def create_project(
    app: str,
    project_root: Path
) -> bool:
    args = [
        "uv",
        "init",
        "--name",
        app,
        "--no-workspace",
        "--app"
    ]

    process = subprocess.run(
        args,
        cwd=project_root,
        check=True
    )

    if process.returncode != 0:
        raise Exception(f"Error initializing project: {process.stderr.decode('utf-8')}")

    return os.path.exists(os.path.join(app, "pyproject.toml"))

def add_dependencies(project_root: Path, dependencies: list[str], dev: bool = False):
    """Add selected dependencies"""
    args = ["uv", "add"]
    args.extend(dependencies)

    if dev:
        args.append("--dev")

    # Run the installation process
    process = subprocess.Popen(
        args, cwd=project_root, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise Exception(f"Error installing dependencies: {stderr.decode('utf-8')}")

    decoded_stdout = stdout.decode("utf-8", errors="replace")
    print(decoded_stdout)

