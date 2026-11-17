#!/usr/bin/env python3
"""Turn a video URL into a short, timestamped note with few Claude tokens.

Order (cheapest first): cache -> captions (free) -> Gemini reads the video.
Claude only ever reads the final note printed on stdout.

Usage:
  python learn_video.py URL [--start 1:30 --end 8:00] [--force-video]
                            [--focus "what to look for"] [--no-save] [--refresh]
Progress goes to stderr. The note goes to stdout.
"""
import argparse, json, os, re, sys, hashlib
from pathlib import Path

CACHE = Path(os.environ.get("LFV_CACHE", Path.home() / ".cache" / "learn-from-video"))
NOTES = Path(os.environ.get("LFV_NOTES", r"C:\Users\Arun\Dropbox\Research\video-notes"))
MODEL = os.environ.get("LFV_MODEL", "gemini-3.5-flash")
PROMPT_FILE = Path(__file__).resolve().parent.parent / "references" / "note-template.md"
LONG_VIDEO_SEC = 45 * 60  # warn above this


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def to_sec(t):
    if t is None:
        return None
    parts = [float(p) for p in str(t).split(":")]
    s = 0.0
    for p in parts:
        s = s * 60 + p
    return s


def fmt(sec):
    sec = int(sec)
    h, r = divmod(sec, 3600)
    m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def probe(url):
    import yt_dlp
    with yt_dlp.YoutubeDL({"quiet": True, "skip_download": True, "no_warnings": True}) as y:
        info = y.extract_info(url, download=False)
    if info.get("entries"):  # search or playlist: use the first video
        info = info["entries"][0]
    return info


def pick_caption(info, lang):
    """Return (kind, url) for a json3 caption track, preferring human captions."""
    for kind, key in (("manual", "subtitles"), ("auto", "automatic_captions")):
        tracks = info.get(key) or {}
        langs = [l for l in tracks if l == lang or l.startswith(lang + "-") or l == lang + "-orig"]
        langs.sort(key=lambda l: (l != lang, l))
        for l in langs:
            for f in tracks[l]:
                if f.get("ext") == "json3":
                    return kind, f["url"]
    return None, None


def get_transcript(info, lang, start, end):
    import urllib.request
    kind, cap_url = pick_caption(info, lang)
    if not cap_url:
        return None, None
    with urllib.request.urlopen(cap_url, timeout=60) as r:
        data = json.load(r)
    lines, last_bucket = [], -1
    for ev in data.get("events", []):
        if "segs" not in ev:
            continue
        t = ev.get("tStartMs", 0) / 1000
        if start is not None and t < start:
            continue
        if end is not None and t > end:
            continue
        text = "".join(s.get("utf8", "") for s in ev["segs"]).replace("\n", " ").strip()
        if not text or text == "[Music]":
            continue
        bucket = int(t // 30)  # one timestamp per ~30 s keeps tokens low
        if bucket != last_bucket:
            lines.append(f"\n[{fmt(t)}] ")
            last_bucket = bucket
        lines.append(text + " ")
    txt = re.sub(r"[ \t]+", " ", "".join(lines)).strip()
    return kind, txt


def gemini_client():
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        sys.exit("ERROR: set GEMINI_API_KEY (paid key, not Gemini CLI login).")
    from google import genai
    return genai.Client(api_key=key)


def make_note(info, source_text, url, mode, focus, start, end, force_video):
    from google.genai import types
    client = gemini_client()
    template = PROMPT_FILE.read_text(encoding="utf-8")
    head = (f"{template}\n\nVideo title: {info.get('title')}\nChannel: {info.get('uploader')}\n"
            f"URL: {url}\nDuration: {fmt(info.get('duration') or 0)}\n")
    if focus:
        head += f"Focus especially on: {focus}\n"
    if mode == "captions":
        contents = head + "\nTRANSCRIPT (timestamps in [m:ss]):\n" + source_text
    else:
        vm = None
        if start is not None or end is not None:
            vm = types.VideoMetadata(
                start_offset=f"{int(start or 0)}s",
                end_offset=f"{int(end)}s" if end else None)
        part = types.Part(file_data=types.FileData(file_uri=url), video_metadata=vm)
        contents = types.Content(parts=[part, types.Part(text=head +
            "\nYou are watching the video itself. Capture what is shown on screen "
            "(code, commands, UI clicks, slides), not only what is said.")])
    resp = client.models.generate_content(model=MODEL, contents=contents)
    u = getattr(resp, "usage_metadata", None)
    if u:
        log(f"gemini tokens: in={u.prompt_token_count} out={u.candidates_token_count}")
    return resp.text.strip()


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "video").lower()).strip("-")[:50]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--start"); ap.add_argument("--end")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--focus")
    ap.add_argument("--force-video", action="store_true", help="skip captions, let Gemini watch")
    ap.add_argument("--refresh", action="store_true", help="ignore cache")
    ap.add_argument("--no-save", action="store_true")
    a = ap.parse_args()
    start, end = to_sec(a.start), to_sec(a.end)

    key = hashlib.md5(json.dumps([a.start, a.end, a.focus, a.force_video, a.lang]).encode()).hexdigest()[:8]
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})", a.url)
    if m and not a.refresh:  # cache check BEFORE touching YouTube
        early = CACHE / m.group(1) / f"note-{key}.md"
        if early.exists():
            log("cache hit (no network, no API call).")
            cached = early.read_text(encoding="utf-8")
            if not a.no_save:
                t = re.search(r'^title: "?(.*?)"?$', cached, re.M)
                NOTES.mkdir(parents=True, exist_ok=True)
                (NOTES / f"{m.group(1)}-{slug(t.group(1) if t else None)}.md").write_text(cached, encoding="utf-8")
            print(cached)
            return
    log("1/4 probing video (no download)...")
    info = probe(a.url)
    vid = info["id"]
    dur = info.get("duration") or 0
    cdir = CACHE / vid
    cdir.mkdir(parents=True, exist_ok=True)
    cfile = cdir / f"note-{key}.md"
    if cfile.exists() and not a.refresh:
        log("cache hit: no API call made.")
        cached = cfile.read_text(encoding="utf-8")
        if not a.no_save:  # restore the saved copy if it was deleted
            NOTES.mkdir(parents=True, exist_ok=True)
            (NOTES / f"{vid}-{slug(info.get('title'))}.md").write_text(cached, encoding="utf-8")
        print(cached)
        return
    if dur > LONG_VIDEO_SEC and start is None and end is None:
        log(f"NOTE: video is {fmt(dur)} long. Consider --start/--end for a focused note.")

    mode, text, kind = "video", None, None
    if not a.force_video:
        log("2/4 looking for captions...")
        kind, text = get_transcript(info, a.lang, start, end)
        if text and len(text) > 200:
            mode = "captions"
            log(f"   found {kind} captions, {len(text.split())} words.")
        else:
            log("   no usable captions; Gemini will watch the video.")
    log(f"3/4 writing note ({mode}) with {MODEL}...")
    note = make_note(info, text, info.get("webpage_url") or a.url, mode, a.focus, start, end, a.force_video)

    meta = (f"---\ntitle: {json.dumps(info.get('title'), ensure_ascii=False)}\nurl: {a.url}\nchannel: {json.dumps(info.get('uploader'))}\n"
            f"duration: {fmt(dur)}\nsource: {mode}{'/' + kind if kind else ''}\n"
            f"range: {a.start or 'start'}-{a.end or 'end'}\n---\n\n")
    full = meta + note + "\n"
    cfile.write_text(full, encoding="utf-8")
    if not a.no_save:
        NOTES.mkdir(parents=True, exist_ok=True)
        out = NOTES / f"{vid}-{slug(info.get('title'))}.md"
        out.write_text(full, encoding="utf-8")
        log(f"4/4 saved: {out}")
    print(full)


if __name__ == "__main__":
    main()
