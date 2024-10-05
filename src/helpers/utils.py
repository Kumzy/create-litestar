from pathlib import Path

def jinja_to_file(resource_path: Path, resource_name: str) -> bool:
    target_file_name = f"{resource_path}/{resource_name[:-3] if resource_name.endswith('.j2') else resource_name}"