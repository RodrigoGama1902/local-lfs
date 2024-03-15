import argparse

from .core import push, pull, status
from pathlib import Path

from typing import Any
from .config import load_config


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Local LFS, a simple local git-lfs alternative"
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-command help")

    _push_parser(subparsers)
    _pull_parser(subparsers)
    _status_parser(subparsers)

    args = parser.parse_args()
    config = load_config(args)

    match args.command:
        case "push":
            push(Path(config.src_path), Path(config.dest_path), config.include)
        case "pull":
            pull(
                Path(config.src_path),
                Path(config.dest_path),
            )
        case "status":
            status(
                Path(config.src_path),
                Path(config.dest_path),
                config.include,
            )
        case _:
            raise ValueError(f"Unknown command: {args.func}")


def _push_parser(subparsers: Any) -> None:
    """Add push subparser to the main parser"""

    push_parser = subparsers.add_parser("push", help="Push changes to local repository")
    _add_common_arguments(push_parser)


def _pull_parser(subparsers: Any) -> None:
    """Add pull subparser to the main parser"""

    pull_parser = subparsers.add_parser(
        "pull", help="Pull changes from local repository"
    )
    _add_common_arguments(pull_parser)


def _status_parser(subparsers: Any) -> None:
    """Add status subparser to the main parser"""

    status_parser = subparsers.add_parser(
        "status", help="Check the status of the local repository"
    )
    _add_common_arguments(status_parser)


def _add_common_arguments(parser: argparse.ArgumentParser) -> None:
    """Add common arguments to the parser"""

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
