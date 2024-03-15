from pathlib import Path

import shutil

from dataclasses import dataclass, field
from enum import Enum, auto


class ChangeType(Enum):
    ADD = auto()
    MODIFY = auto()
    DELETE = auto()


@dataclass
class FileChange:

    path: Path
    change_type: ChangeType = field(default=ChangeType.ADD)


def _check_changes(
    root_dir: Path, src_path: Path, dest_path: Path, include: list[str]
) -> list[FileChange]:
    """Check changes between src_path and dest_path"""

    # TODO: Implement right
    raise NotImplementedError

    changed_files: list[FileChange] = []
    for item in src_path.iterdir():
        dest_item = dest_path / item.name
        if item.is_file() and _check_is_include(root_dir, item, include):
            if not dest_item.exists():
                changed_files.append(FileChange(item, ChangeType.ADD))

            elif item.stat().st_mtime > dest_item.stat().st_mtime:
                changed_files.append(FileChange(item, ChangeType.MODIFY))

        elif item.is_dir() and _check_is_include(root_dir, item, include):
            changed_files.extend(_check_changes(root_dir, item, dest_item, include))

    for item in dest_path.iterdir():
        src_item = src_path / item.name
        if item.is_file() and _check_is_include(dest_path, item, include):
            if not src_item.exists():
                changed_files.append(FileChange(item, ChangeType.DELETE))

        elif item.is_dir() and _check_is_include(dest_path, item, include):
            changed_files.extend(_check_changes(root_dir, src_item, item, include))

    return changed_files


def _check_is_include(root_dir: Path, item: Path, include: list[str]) -> bool:
    """Check if the item is in the include path"""

    if not include:
        return True

    for path in include:
        if str(item.resolve()).startswith(str(Path(root_dir, path).resolve())):
            return True
        elif (
            str(Path(root_dir, path).resolve()).startswith(str(item.resolve()))
            and item.is_dir()
        ):
            return True
    return False


def _copy_files(
    root_dir: Path, src_dir: Path, dest_dir: Path, include: list[str]
) -> None:
    """Copy files from src_dir to dest_dir, only if they are in the include"""

    src_path = Path(src_dir)
    if not src_path.exists():
        print(f"Source directory '{src_path}' does not exist.")
        return

    dest_path = Path(dest_dir)
    dest_path.mkdir(parents=True, exist_ok=True)

    for item in src_path.iterdir():
        dest_item = dest_path / item.name
        if item.is_file() and _check_is_include(root_dir, item, include):
            print(f"Copying {item} to {dest_item}")
            shutil.copy2(item, dest_item)
        elif item.is_dir() and _check_is_include(root_dir, item, include):
            print(f"Copying {item} to {dest_item}")
            _copy_files(root_dir, item, dest_item, include)


def _delete_empty_folders(path: Path, src_path: Path):
    """Delete empty folders recursively"""

    for item in path.iterdir():
        if item.is_dir():
            _delete_empty_folders(item, src_path)

    if not list(path.iterdir()) and not src_path == path:
        print(f"Removing empty directory {path}")
        path.rmdir()


def push(src_path: Path, dest_path: Path, include: list[str] = []):
    """Copy files from src_path to dest_path, only if they are in the include"""

    if not src_path.exists():
        raise FileNotFoundError(f"Source directory '{src_path}' does not exist.")

    _copy_files(src_path, src_path, dest_path, include)
    _delete_empty_folders(dest_path, src_path)


def pull(src_path: Path, dest_path: Path):
    """Copy files from src_path to dest_path"""

    if not src_path.exists():
        raise FileNotFoundError(f"Source directory '{src_path}' does not exist.")

    _copy_files(src_path, src_path, dest_path, [])


def status(src_path: Path, dest_path: Path, include: list[str] = []):
    """Check changes between src_path and dest_path"""

    for change in _check_changes(src_path, src_path, dest_path, include):
        print(change.path, change.change_type)
