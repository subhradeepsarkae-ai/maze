# Maze — Universal CLI Video Downloader

# Maze — Universal CLI Video Downloader

> **Command:** `mz <url> [--high | --fast] [--mute] [-o DIR]`  
> **Also:** `mz --clip [--high | --fast] [--mute] [-o DIR]`  
> **Tagline:** One command to download from YouTube, Instagram, TikTok, Twitter, Facebook, and 1000+ sites.

---

## Quick Start

```bash
mz https://youtube.com/watch?v=...
mz https://instagram.com/p/...
mz https://youtube.com/watch?v=... --high
mz https://youtube.com/watch?v=... --fast --mute
mz --clip --high
```

---

## Installation

### One-liner (works in CMD & PowerShell)

```cmd
pip install git+https://github.com/subhradeepsarkae-ai/maze.git
```

### Script installer (PowerShell)

```powershell
powershell -c "iwr -useb https://raw.githubusercontent.com/subhradeepsarkae-ai/maze/main/install.ps1 | iex"
```

### Manual

```bash
git clone https://github.com/subhradeepsarkae-ai/maze.git
cd maze
pip install .
```

After install, `mz` is available **globally** from any terminal.

---

## All Commands

### Direct URL

| Command | Menu? | Quality |
|---|---|---|
| `mz <url>` | ✅ Yes | User picks |
| `mz <url> --mute` | ✅ Yes | User picks, video only |
| `mz <url> --high` | ❌ No | Best available |
| `mz <url> --high --mute` | ❌ No | Best video only |
| `mz <url> --fast` | ❌ No | 480p (or closest) |
| `mz <url> --fast --mute` | ❌ No | 480p video only |
| `mz <url> --high --fast` | ❌ No | `--high` wins |
| `mz <url> -o "C:\path"` | ✅ Yes | Custom output dir |
| `mz <url> --high -o "C:\path"` | ❌ No | Best + custom dir |

### Clipboard URL

| Command | Menu? | Quality |
|---|---|---|
| `mz --clip` | ✅ Yes | Reads clipboard, user picks |
| `mz --clip --mute` | ✅ Yes | Clipboard, user picks video only |
| `mz --clip --high` | ❌ No | Clipboard, best |
| `mz --clip --high --mute` | ❌ No | Clipboard, best video only |
| `mz --clip --fast` | ❌ No | Clipboard, 480p |
| `mz --clip --fast --mute` | ❌ No | Clipboard, 480p video only |

> **Flags can be in any order** — `--mute --high <url>` works the same as `<url> --high --mute`.

---

## How It Works

| Step | What happens |
|------|-------------|
| 1 | Run `mz <url>` |
| 2 | Fetches video metadata via **yt-dlp** (extracts title, duration, available formats) |
| 3 | Shows a **rich interactive menu** with quality options (skipped with `--high`/`--fast`) |
| 4 | You pick a quality (or cancel with `q`) |
| 5 | Downloads with a **live progress bar** (speed, ETA, percentage) |
| 6 | Saves to current directory (or `-o` path) |

---

## Quality Options

The menu dynamically shows **only the resolutions that exist** for that video:

| # | Quality | Notes |
|---|---------|-------|
| 1 | 144p | Lowest |
| 2 | 240p | |
| 3 | 360p | |
| 4 | 480p | |
| 5 | 720p | HD |
| 6 | 1080p | Full HD |
| 7 | 2K | 1440p |
| 8 | 4K | 2160p |
| 9 | 8K | 4320p (if exists) |
| N | Best Available | Auto-selects highest quality |
| N+1 | Audio Only | Download as MP3/M4A |

With `--mute`: shows only **video-only streams** (no audio track).

---

## Tech Stack

| Component | Library |
|-----------|---------|
| Download engine | [yt-dlp](https://github.com/yt-dlp/yt-dlp) (supports 1000+ sites) |
| CLI framework | Python `argparse` |
| Terminal UI | [rich](https://github.com/Textualize/rich) (tables, panels, progress bars) |
| Language | Python 3.8+ |

---

## Project Structure

```
D:\maze\
├── maze/
│   ├── __init__.py          # Package marker
│   ├── cli.py               # Entry point: argparse, main loop, --high/--fast/--clip
│   ├── downloader.py        # yt-dlp wrapper (fetch, format spec, download)
│   └── ui.py                # Rich UI (header, menu, progress bar)
├── setup.py                 # pip install config + console_scripts entry
├── install.ps1              # Windows one-liner installer
├── CHECKPOINT.md            # This file
└── .gitignore
```

---

## Key Files Explained

### `maze/cli.py`
- Parses `url`, `--mute`, `--high`, `--fast`, `--clip`, `-o` with `argparse`
- `--clip` reads URL from Windows clipboard via PowerShell
- `--high` / `--fast` bypass the quality menu and auto-download
- Calls `downloader.fetch_info()` → `downloader.get_format_spec()` → `downloader.download()`
- Handles `KeyboardInterrupt` gracefully

### `maze/downloader.py`
- `fetch_info(url)` — extracts metadata + available resolutions via yt-dlp
- `get_format_spec(resolution, mute, audio_only, has_ffmpeg)` — builds yt-dlp format selector
  - Normal + ffmpeg: `bestvideo[height<=H]+bestaudio/best[height<=H]`
  - No ffmpeg: `best[height<=H]` (combined format, guaranteed audio)
  - Mute: `bestvideo[height<=H][vcodec!=?av01]/bestvideo[height<=H]`
  - Audio only: `bestaudio/best`
  - Best + ffmpeg: `bestvideo+bestaudio/best`
- `download(url, format_spec, output_dir, progress_hook)` — downloads, merges via ffmpeg to AAC (Opus→AAC conversion for Windows Media Player compatibility)

### `maze/ui.py`
- Rich `Panel` for header (title, source, duration)
- Rich `Table` for quality menu (numbered list, color-coded)
- Rich `Progress` bar with download column, transfer speed, time remaining
- Functions: `show_header()`, `show_resolution_menu()`, `parse_choice()`, `create_progress()`

### `setup.py`
- Defines `mz=maze.cli:main` as a `console_scripts` entry point
- Dependencies: `yt-dlp>=2023.0.0`, `rich>=13.0.0`

---

## Format Specs

| Scenario | Format string | Notes |
|---|---|---|
| Normal + ffmpeg | `bestvideo[height<=H]+bestaudio/best[height<=H]` | Merged via ffmpeg |
| Normal no ffmpeg | `best[height<=H]` | Single combined file |
| Mute | `bestvideo[height<=H][vcodec!=?av01]/bestvideo[height<=H]` | Skips AV1 codec (avoids 416 errors) |
| Audio only | `bestaudio/best` | MP3/M4A |
| Best + ffmpeg | `bestvideo+bestaudio/best` | Highest quality |
| Best no ffmpeg | `best` | Highest combined |

---

## Edge Cases Handled

| Scenario | Behavior |
|----------|----------|
| Invalid URL | Error message, exits |
| Private/deleted video | "No formats found" error |
| No ffmpeg | Falls back to single-file formats (always has audio) |
| Opus audio codec | Auto-converted to AAC (plays on any Windows media player) |
| AV1 video 416 error | Skips AV1 codec, picks next best format |
| Empty clipboard with `--clip` | "Clipboard is empty" error |
| Ctrl+C during download | Clean exit, no crash |
| `--mute` with no video-only stream | Falls back to `bestvideo` |
| Unknown duration | Shows `--:--` |
| Long titles | Truncated with `...` |
| No resolutions found | Meaningful error, exits |

---

## Supported Sites (via yt-dlp)

YouTube, Instagram, TikTok, Twitter/X, Facebook, Twitch, Vimeo, Dailymotion, Reddit, LinkedIn, Pinterest, Snapchat, Telegram, WhatsApp, and **1000+ more**. Full list at [yt-dlp's supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/docs/supportedsites.md).

---

## Changelog

### v1.0.0 — 2026-06-05
- Initial release
- `mz <url>` with interactive quality picker
- `--mute` flag for video-only downloads
- `--high` / `--fast` flags to bypass menu
- `--clip` flag to read URL from clipboard
- Rich terminal UI with live progress bar
- Opus→AAC audio conversion for Windows Media Player compatibility
- Windows installer script
