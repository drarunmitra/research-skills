"""Command dispatch. Every command prints short output."""
import argparse
from pathlib import Path

from . import convert, outline
from .extract import DocError


def _convert(args) -> int:
    meta = convert.convert(Path(args.file), force=args.force)
    kind = "small" if meta["small"] else "mapped"
    print(f"{meta['name']}: {meta['pages']} pages, ~{meta['tokens']} tokens, "
          f"{kind}, cache {meta['sha'][:8]}")
    for w in meta["warnings"][:5]:
        print(f"warning: {w}")
    return 0


def _map(args) -> int:
    meta = convert.convert(Path(args.file))
    print(outline.render_map(outline.build_map(meta["sha"]), meta))
    return 0


def run(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="docread")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("convert")
    c.add_argument("file")
    c.add_argument("--force", action="store_true")
    c.set_defaults(fn=_convert)
    m = sub.add_parser("map")
    m.add_argument("file")
    m.set_defaults(fn=_map)
    args = ap.parse_args(argv)
    try:
        return args.fn(args)
    except DocError as e:
        print(f"error: {e}")
        return 2
