"""Content-addressed cache."""
import hashlib
import json
from pathlib import Path

from . import env


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def entry_dir(sha: str) -> Path:
    return env.home() / "cache" / sha


def load_meta(sha: str) -> dict | None:
    p = entry_dir(sha) / "meta.json"
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))
