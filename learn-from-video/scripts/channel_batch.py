#!/usr/bin/env python3
"""Note every video of a channel/playlist, then write INDEX.md.

Usage: python channel_batch.py CHANNEL_URL OUT_DIR [--workers 4] [--limit N]
Prints one progress line per video on stdout: "done/total status id title".
Failed videos are listed in OUT_DIR/FAILED.txt and can be rerun (cache skips finished ones).
"""
import argparse, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent


def list_videos(url):
    out = subprocess.run([sys.executable, "-m", "yt_dlp", "--flat-playlist", "--print",
                          "%(id)s\t%(duration_string)s\t%(title)s", url],
                         capture_output=True).stdout.decode("utf-8", "replace")
    rows = [l.split("\t", 2) for l in out.splitlines() if l.count("\t") == 2]
    return rows


def run_one(vid, out_dir):
    env = dict(os.environ, LFV_NOTES=str(out_dir), PYTHONIOENCODING="utf-8")
    for attempt in (1, 2):
        r = subprocess.run([sys.executable, str(HERE / "learn_video.py"),
                            f"https://www.youtube.com/watch?v={vid}"],
                           capture_output=True, text=True, encoding="utf-8", env=env)
        if r.returncode == 0:
            return True, ""
        time.sleep(5 * attempt)
    return False, (r.stderr.strip().splitlines() or ["unknown error"])[-1][:200]


def tldr(path):
    t = path.read_text(encoding="utf-8")
    m = re.search(r"## TL;DR\s*\n(.+?)\n\s*\n", t, re.S)
    return (m.group(1).strip() if m else "").replace("\n", " ")


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("url"); ap.add_argument("out_dir")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--limit", type=int)
    a = ap.parse_args()
    out = Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)
    vids = list_videos(a.url)[: a.limit]
    total, done, failed = len(vids), 0, []
    print(f"0/{total} start, {a.workers} workers", flush=True)
    with ThreadPoolExecutor(a.workers) as ex:
        futs = {ex.submit(run_one, v[0], out): v for v in vids}
        for f in as_completed(futs):
            v = futs[f]; ok, err = f.result(); done += 1
            if not ok:
                failed.append((v, err))
            print(f"{done}/{total} {'ok' if ok else 'FAIL'} {v[0]} {v[2][:60]} {err}", flush=True)
    lines = [f"# Channel index ({total} videos)\n", f"Source: {a.url}\n"]
    for vid, dur, title in vids:
        notes = list(out.glob(f"{vid}-*.md"))
        s = tldr(notes[0]) if notes else "(no note)"
        link = notes[0].name if notes else ""
        lines.append(f"- **{title}** ({dur}) [{vid}]({link}): {s}")
    (out / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / "FAILED.txt").write_text("\n".join(f"{v[0]} {v[2]} :: {e}" for v, e in failed), encoding="utf-8")
    print(f"finished: {total - len(failed)} ok, {len(failed)} failed. Index: {out / 'INDEX.md'}", flush=True)


if __name__ == "__main__":
    main()
