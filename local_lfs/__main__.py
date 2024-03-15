import argparse
import sys
import toml

from .core import push, pull, status
from pathlib import Path

from dataclasses import dataclass, field
from typing import List, Any


@dataclass
class Config:
    dest_path: str = field(default="")
    src_path: str = field(default=".")
    include: List[str] = field(default_factory=list)

    def update_from_args(self, args: argparse.Namespace) -> None:
        for key, value in vars(args).items():
            if value is not None:
                setattr(self, key, value)

    def check(self) -> None:
        if not self.src_path:
            raise ValueError("src_path is required")
        if not self.dest_path:
            raise ValueError("dest_path is required")


def _load_toml(root: Path) -> dict[str, Any]:
    path = root / "pyproject.toml"
    if not path.exists():
        return {}

    with open(path, "r") as f:
        try:
            return toml.load(f)["tool"]["local_lfs"]
        except KeyError:
            return {}


def push_cmd(config: Config) -> None:
    print("Pushing changes to remote repository...")
    push(Path(config.src_path), Path(config.dest_path), config.include)


def pull_cmd(config: Config) -> None:
    print("Pulling changes from remote repository...")
    pull(
        Path(config.src_path),
        Path(config.dest_path),
    )


def status_cmd(config: Config) -> None:
    status(
        Path(config.src_path),
        Path(config.dest_path),
        config.include,
    )


def main() -> None:

    parser = argparse.ArgumentParser(
        description="Simple CLI like GitHub with push and pull commands"
    )
    subparsers = parser.add_subparsers()

    push_parser = subparsers.add_parser(
        "push", help="Push changes to remote repository"
    )
    push_parser.add_argument(
        "src_path",
        nargs="?",
        help="Source path of the repository (default: current directory)",
    )
    push_parser.add_argument(
        "--dest_path", "-d", help="Destination path of the repository"
    )
    push_parser.add_argument(
        "--include",
        "-i",
        nargs="+",
        default=[],
        help="Include paths for the operation (default: none)",
    )
    push_parser.set_defaults(func=push_cmd)

    pull_parser = subparsers.add_parser(
        "pull", help="Pull changes from remote repository"
    )
    pull_parser.add_argument(
        "src_path",
        nargs="?",
        help="Source path of the repository (default: current directory)",
    )
    pull_parser.add_argument(
        "--dest_path", "-d", help="Destination path of the repository"
    )
    pull_parser.add_argument(
        "--include",
        "-i",
        nargs="+",
        default=[],
        help="Include paths for the operation (default: none)",
    )
    pull_parser.set_defaults(func=pull_cmd)

    status_parser = subparsers.add_parser(
        "status", help="Pull changes from remote repository"
    )
    status_parser.add_argument(
        "src_path",
        nargs="?",
        help="Source path of the repository (default: current directory)",
    )
    status_parser.add_argument(
        "--dest_path", "-d", help="Destination path of the repository"
    )
    status_parser.add_argument(
        "--include",
        "-i",
        nargs="+",
        default=[],
        help="Include paths for the operation (default: none)",
    )
    status_parser.set_defaults(func=status_cmd)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    src_path = Path(args.src_path) if args.src_path else Path.cwd()
    toml_data = _load_toml(src_path)

    config = Config(**toml_data)
    config.update_from_args(args)
    config.check()

    args.func(config)


if __name__ == "__main__":
    main()
