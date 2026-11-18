"""Command dispatch. Every command prints short output."""
import argparse
import re
from pathlib import Path

from . import convert, outline, readcmd
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


def _read(args) -> int:
    meta = convert.convert(Path(args.file))
    if args.section:
        print(readcmd.read_section(meta["sha"], args.section))
    elif args.pages:
        m = re.fullmatch(r"(\d+)(?:-(\d+))?", args.pages)
        if not m:
            raise DocError("--pages needs A-B, for example 3-5")
        a = int(m.group(1))
        print(readcmd.read_pages(meta["sha"], a, int(m.group(2) or a)))
    elif args.all:
        print(readcmd.read_all(meta["sha"], meta, yes=args.yes))
    else:
        raise DocError("choose --section TEXT, --pages A-B or --all")
    return 0


def _grep(args) -> int:
    meta = convert.convert(Path(args.file))
    print(readcmd.grep(meta["sha"], args.text))
    return 0


def _page_image(args) -> int:
    convert.convert(Path(args.file))
    print(readcmd.page_image(Path(args.file), args.page))
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
    r = sub.add_parser("read")
    r.add_argument("file")
    r.add_argument("--section")
    r.add_argument("--pages")
    r.add_argument("--all", action="store_true")
    r.add_argument("--yes", action="store_true")
    r.set_defaults(fn=_read)
    g = sub.add_parser("grep")
    g.add_argument("file")
    g.add_argument("text")
    g.set_defaults(fn=_grep)
    pi = sub.add_parser("page-image")
    pi.add_argument("file")
    pi.add_argument("page", type=int)
    pi.set_defaults(fn=_page_image)
    args = ap.parse_args(argv)
    try:
        return args.fn(args)
    except DocError as e:
        print(f"error: {e}")
        return 2
