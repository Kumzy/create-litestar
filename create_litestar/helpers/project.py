import os
import subprocess
from pathlib import Path
from subprocess import CalledProcessError
from typing import Any
from copier import run_copy


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
        "--app",
        "--no-readme"
    ]
    try:
        process = subprocess.run(
            args,
            cwd=project_root,
            check=True
        )
    except CalledProcessError:
        raise Exception(f"Error initializing project: {process.stderr.decode('utf-8')}")

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

def copy_project(template_path: Path, project_root: Path, data: dict[str: Any]) -> bool:

    # Run copier
    run_copy(
        src_path=str(template_path),
        dst_path=project_root,
        data=data,
        cleanup_on_error=True,
        quiet=True
    )

def remove_files(project_root: Path):
   # Remove files, especially unwanted files created by `uv init`
    files = ['hello.py']


    for file in files:
        try:
            if os.path.exists(project_root.joinpath(file)):
                os.remove(project_root.joinpath(file))
                print(f"File {file} has been removed successfully")
        except FileNotFoundError:
            print(f"File {file} does not exist")
        except PermissionError:
            print(f"Permission denied: unable to delete {file}")
        except Exception as e:
            print(f"An error occurred while trying to delete {file}: {e}")