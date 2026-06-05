# Maze — Universal CLI Video Downloader

> **Command:** `mz <url> [options]`  
> **Tagline:** One command to download from YouTube, Instagram, TikTok, Twitter, Facebook, and 1000+ sites.

---

## Quick Start

```bash
mz https://youtube.com/watch?v=...
mz https://instagram.com/p/...
mz https://youtube.com/watch?v=... --mute
mz https://youtube.com/watch?v=... -o "C:\Videos"
```

---

## Installation

### One-liner installer (Windows PowerShell)

```powershell
powershell -c "iwr -useb https://raw.githubusercontent.com/subhradeepsarkae-ai/maze/main/install.ps1 | iex"
```

### Manual install

```bash
git clone https://github.com/subhradeepsarkae-ai/maze.git
cd maze
pip install .
```

This makes the `mz` command available **globally** from any terminal.

---

## How It Works

| Step | What happens |
|------|-------------|
| 1 | Run `mz <url>` |
| 2 | Fetches video metadata via **yt-dlp** (extracts title, duration, available formats) |
| 3 | Shows a **rich interactive menu** with quality options |
| 4 | You pick a quality (or cancel with `q`) |
| 5 | Downloads with a **live progress bar** (speed, ETA, percentage) |
| 6 | Saves to current directory (or `-o` path) |

---

## Commands

| Command | Description |
|---------|-------------|
| `mz <url>` | Fetch video, show quality picker, download |
| `mz <url> --mute` | Download video **without audio** (video-only stream) |
| `mz <url> -o "path"` | Save to a custom directory |
| `mz --help` | Show help |

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
│   ├── cli.py               # Entry point: argparse, main loop
│   ├── downloader.py         # yt-dlp wrapper (fetch_info, get_format_spec, download)
│   └── ui.py                # Rich UI (header, menu, progress bar)
├── setup.py                 # pip install config + console_scripts entry
├── install.ps1              # Windows one-liner installer
├── CHECKPOINT.md            # This file
└── .gitignore
```

---

## Key Files Explained

### `maze/cli.py`
- Parses `url`, `--mute`, `-o` with `argparse`
- Calls `downloader.fetch_info()` to get metadata
- Calls `ui.show_resolution_menu()` for interactive quality pick
- Converts choice to format spec with `downloader.get_format_spec()`
- Runs `downloader.download()` with a rich progress hook
- Handles `KeyboardInterrupt` gracefully

### `maze/downloader.py`
- `fetch_info(url)` — extracts metadata + available resolutions via yt-dlp
- `get_format_spec(resolution, mute, audio_only)` — builds yt-dlp format selector
  - Normal: `bestvideo[height<=H]+bestaudio/best[height<=H]`
  - Mute: `bestvideo[height<=H]`
  - Audio: `bestaudio/best`
  - Best: `bestvideo+bestaudio/best`
- `download(url, format_spec, output_dir, progress_hook)` — downloads with yt-dlp, merges via ffmpeg if available

### `maze/ui.py`
- Rich `Panel` for header (title, source, duration)
- Rich `Table` for quality menu (numbered list, color-coded)
- Rich `Progress` bar with download column, transfer speed, time remaining
- Functions: `show_header()`, `show_resolution_menu()`, `parse_choice()`, `create_progress()`

### `setup.py`
- Defines `mz=maze.cli:main` as a `console_scripts` entry point
- Dependencies: `yt-dlp>=2023.0.0`, `rich>=13.0.0`

---

## Edge Cases Handled

| Scenario | Behavior |
|----------|----------|
| Invalid URL | Shows error message, exits |
| Private/deleted video | "No formats found" error |
| No ffmpeg | Falls back to single-file formats (no merge) |
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
- Rich terminal UI with live progress bar
- Windows installer script
