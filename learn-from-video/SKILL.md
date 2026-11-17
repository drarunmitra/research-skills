---
name: learn-from-video
description: Use when the user shares a YouTube link or tutorial video URL and wants Claude to learn from it, summarize it, extract steps or commands, or keep notes, and token cost matters. Also use for "watch this video", "what does this tutorial say", "take notes on this lecture".
---

# Learn from video (low token)

Turns a video URL into a short timestamped note. A cheap Gemini call reads the long transcript or the video. Claude reads only the ~400-word note.

## Run it

```bash
python ~/.claude/skills/learn-from-video/scripts/learn_video.py "<URL>" [options]
```

The note prints on stdout. Progress prints on stderr. A copy saves to `C:\Users\Arun\Dropbox\Research\video-notes\<id>-<slug>.md`.

| Need | Option |
|---|---|
| Only part of a long video | `--start 12:00 --end 25:30` |
| Look for one thing | `--focus "the model formula"` |
| Screen matters (code, UI, slides) or no captions | `--force-video` (Gemini watches; this happens on its own when no captions exist) |
| Redo, ignore cache | `--refresh` |
| Do not save a file | `--no-save` |

## How it saves tokens

1. Cache by video id and options. A repeat run makes no API call.
2. Free YouTube captions first. No download.
3. Gemini (`gemini-3.5-flash`, override with `LFV_MODEL`) writes the note, not Claude.
4. Fixed note template: `references/note-template.md`. Edit it to change the note shape.

## Rules for Claude

- Read the printed note only. Do not open the raw transcript or cache files unless the user asks for more detail.
- For a detail the note lacks, rerun with `--start/--end` and `--focus`. Do not rerun the whole video.
- Video over 45 min: suggest a time range first.
- Captions are auto-generated for most videos. Code and commands from speech may be wrong. For code-heavy tutorials, use `--force-video` so Gemini reads the screen.
- Say which source was used (`captions/auto`, `captions/manual`, or `video`) when you report back.

## Setup (once)

`pip install yt-dlp google-genai`. `GEMINI_API_KEY` must be set (paid API key; Gemini CLI login does not work). Keep yt-dlp updated: `pip install -U yt-dlp`.

## Limits

- Not tested on private, age-gated, or login-only videos.
- Non-YouTube URLs have captions only if yt-dlp finds them. Otherwise Gemini may refuse the URL. Then download the file with yt-dlp and upload it to Gemini (not built yet).
- No frame extraction yet. Add it only if notes miss visuals.
