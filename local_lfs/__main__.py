import argparse
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


def _push_cmd(config: Config) -> None:
    push(Path(config.src_path), Path(config.dest_path), config.include)


def _pull_cmd(config: Config) -> None:
    pull(
        Path(config.src_path),
        Path(config.dest_path),
    )


def _status_cmd(config: Config) -> None:
    status(
        Path(config.src_path),
        Path(config.dest_path),
        config.include,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Local LFS, a simple local git-lfs alternative"
    )
    subparsers = parser.add_subparsers()

    # Define push command parser
    push_parser = subparsers.add_parser("push", help="Push changes to local repository")
    _add_common_arguments(push_parser)
    push_parser.set_defaults(func=_push_cmd)

    # Define pull command parser
    pull_parser = subparsers.add_parser(
        "pull", help="Pull changes from local repository"
    )
    _add_common_arguments(pull_parser)
    pull_parser.set_defaults(func=_pull_cmd)

    # Define status command parser
    status_parser = subparsers.add_parser(
        "status", help="check the status of the local repository"
    )
    _add_common_arguments(status_parser)
    status_parser.set_defaults(func=_status_cmd)

    args = parser.parse_args()

    src_path = Path(args.src_path) if args.src_path else Path.cwd()
    toml_data = _load_toml(src_path)

    config = Config(**toml_data)
    config.update_from_args(args)
    config.check()

    args.func(config)


def _add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "src_path",
        nargs="?",
        help="Source path of the repository (default: current directory)",
    )
    parser.add_argument("--dest_path", "-d", help="Destination path of the repository")
    parser.add_argument(
        "--include",
        "-i",
        nargs="+",
        default=[],
        help="Include paths for the operation (default: none)",
    )


if __name__ == "__main__":
    main()
