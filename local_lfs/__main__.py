import argparse
import sys


from .core import push, pull, status
from pathlib import Path


def print_args(args: argparse.Namespace) -> None:
    print("Arguments used:")
    for arg, value in vars(args).items():
        print(f"{arg}: {value}")


def push_cmd(args: argparse.Namespace) -> None:
    print_args(args)
    print("Pushing changes to remote repository...")
    push(Path(args.src_path), Path(args.dest_path), args.include_path)


def pull_cmd(args: argparse.Namespace) -> None:
    print_args(args)
    print("Pulling changes from remote repository...")
    pull(
        Path(args.src_path),
        Path(args.dest_path),
    )


def status_cmd(args: argparse.Namespace) -> None:
    print_args(args)
    status(
        Path(args.src_path),
        Path(args.dest_path),
        args.include_path,
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
        default=".",
        help="Source path of the repository (default: current directory)",
    )
    push_parser.add_argument(
        "--dest_path", "-d", required=True, help="Destination path of the repository"
    )
    push_parser.add_argument(
        "--include_path",
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
        default=".",
        help="Source path of the repository (default: current directory)",
    )
    pull_parser.add_argument(
        "--dest_path", "-d", required=True, help="Destination path of the repository"
    )
    pull_parser.add_argument(
        "--include_path",
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
        default=".",
        help="Source path of the repository (default: current directory)",
    )
    status_parser.add_argument(
        "--dest_path", "-d", required=True, help="Destination path of the repository"
    )
    status_parser.add_argument(
        "--include_path",
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
    args.func(args)


if __name__ == "__main__":
    main()
