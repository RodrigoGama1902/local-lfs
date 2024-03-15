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


def load_toml(root: Path) -> dict[str, Any]:
    path = root / "pyproject.toml"
    if not path.exists():
        return {}

    with open(path, "r") as f:
        try:
            return toml.load(f)["tool"]["local_lfs"]
        except KeyError:
            return {}
