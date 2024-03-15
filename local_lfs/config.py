import argparse
import toml

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


def load_config(args: argparse.Namespace) -> Config:

    src_path = Path(args.src_path) if args.src_path else Path.cwd()
    toml_data = _load_toml(src_path)

    config = Config(**toml_data)
    config.update_from_args(args)
    config.check()

    return config
