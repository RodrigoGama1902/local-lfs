import subprocess
from pathlib import Path
from typing import Dict, Any


def _create_directory_structure(path: Path, structure: Dict[str, Any]) -> None:
    """Creates a directory structure based on the input dictionary"""

    for name, value in structure.items():
        if value:
            (path / name).mkdir()
            _create_directory_structure(path / name, value)
            continue
        (path / name).touch()


def _assert_directory_structure(path: Path, expected_structure: Dict[str, Any]) -> None:
    """Asserts that the directory structure is as expected"""

    for item in path.iterdir():
        if item.is_dir():
            assert item.name in expected_structure
            _assert_directory_structure(item, expected_structure[item.name])
        else:
            assert item.name in expected_structure


def _create_tmp_folder(tmp_path: Path, dir_name: str) -> Path:
    """Creates a temporary folder and returns its path"""

    tmp_path = tmp_path / dir_name
    tmp_path.mkdir()
    return tmp_path


def test_push_command(tmp_path: Path):

    src_path = _create_tmp_folder(tmp_path, "src")
    dest_path = _create_tmp_folder(tmp_path, "dest")

    # Create source structure with LFS files
    _create_directory_structure(
        src_path,
        {
            "src": {},
            ".venv": {},
            "tests": {"fixtures": {"file.txt": None}},
        },
    )

    # Create destination structure without LFS files
    result = subprocess.run(
        [
            "local_lfs",
            "push",
            str(src_path),
            "-d",
            str(dest_path),
            "-i",
            "tests/fixtures/",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert len(list(dest_path.iterdir())) > 0

    expected_structure: Dict[str, Any] = {"tests": {"fixtures": {"file.txt": None}}}
    _assert_directory_structure(dest_path, expected_structure)


def test_pull_command(tmp_path: Path):

    src_path = _create_tmp_folder(tmp_path, "src")
    dest_path = _create_tmp_folder(tmp_path, "dest")

    # Create source structure without LFS files
    _create_directory_structure(
        src_path,
        {
            "src": {},
            ".venv": {},
        },
    )

    # Create destination structure with LFS files
    _create_directory_structure(
        dest_path,
        {
            "tests": {"fixtures": {"file.txt": None}},
        },
    )

    result = subprocess.run(
        [
            "local_lfs",
            "push",
            str(src_path),
            "-d",
            str(dest_path),
            "-i",
            "tests/fixtures/",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert len(list(dest_path.iterdir())) > 0

    expected_structure = {
        "src": {},
        ".venv": {},
        "tests": {"fixtures": {"file.txt": None}},
    }

    _assert_directory_structure(dest_path, expected_structure)
