import argparse
import subprocess
import sys

from . import downloader, ui


def _read_clipboard():
    try:
        result = subprocess.run(
            ['powershell', '-command', 'Get-Clipboard'],
            capture_output=True, text=True, check=True, timeout=5
        )
        url = result.stdout.strip()
        if not url:
            ui.show_error("Clipboard is empty.")
            sys.exit(1)
        return url
    except subprocess.TimeoutExpired:
        ui.show_error("Failed to read clipboard (timeout).")
        sys.exit(1)
    except subprocess.SubprocessError:
        ui.show_error("Failed to read clipboard.")
        sys.exit(1)


def _closest_resolution(target, available):
    return min(available, key=lambda r: abs(r - target))


def main():
    try:
        parser = argparse.ArgumentParser(
            prog='mz',
            description='Maze - Universal Video Downloader',
            usage='mz <url> [--high | --fast] [--mute] [-o DIR]\n       mz --clip [--high | --fast] [--mute] [-o DIR]',
        )
        parser.add_argument('url', nargs='?', help='Video URL (YouTube, Instagram, TikTok, etc.)')
        parser.add_argument('--mute', action='store_true', help='Download video without audio track')
        parser.add_argument('--high', action='store_true', help='Download highest quality (bypass menu)')
        parser.add_argument('--fast', action='store_true', help='Download 480p quality (bypass menu)')
        parser.add_argument('--clip', action='store_true', help='Read URL from clipboard')
        parser.add_argument('-o', '--output', default='.', help='Output directory (default: current)')

        args = parser.parse_args()

        url = args.url
        if args.clip:
            url = _read_clipboard()
            ui.console.print(f"[dim]Clipboard URL: {url}[/]")

        if not url:
            parser.print_help()
            sys.exit(1)

        ui.console.print("[bold yellow]Fetching video info...[/]")
        try:
            info = downloader.fetch_info(url)
        except Exception as e:
            ui.show_error(f"Could not fetch video: {e}")
            sys.exit(1)

        ui.show_header(info)

        if not info['resolutions']:
            ui.show_error("No video formats found. The video might be private or unavailable.")
            sys.exit(1)

        resolutions = info['resolutions']

        if args.high:
            resolution = resolutions[-1]
            mute = args.mute
            audio_only = False
            ui.console.print(f"[cyan]High mode:[/] {downloader.RES_LABELS.get(resolution, f'{resolution}p')}")
        elif args.fast:
            resolution = _closest_resolution(480, resolutions)
            mute = args.mute
            audio_only = False
            ui.console.print(f"[cyan]Fast mode:[/] {downloader.RES_LABELS.get(resolution, f'{resolution}p')}")
        else:
            choice = ui.show_resolution_menu(info, mute=args.mute)
            if choice is None:
                ui.console.print("[yellow]Cancelled.[/]")
                sys.exit(0)
            resolution, mute, audio_only = ui.parse_choice(choice, resolutions, args.mute)

        format_spec = downloader.get_format_spec(resolution, mute, audio_only, downloader._has_ffmpeg())

        ui.console.print(f"\n[bold cyan]Downloading...[/]")

        progress = ui.create_progress()

        with progress:
            task = progress.add_task("[cyan]Downloading", name="Downloading", total=None)

            def progress_hook(d):
                if d['status'] == 'downloading':
                    total = d.get('total_bytes') or d.get('total_bytes_estimate')
                    downloaded = d.get('downloaded_bytes', 0)
                    if total:
                        progress.update(task, total=total, completed=downloaded)
                elif d['status'] == 'finished':
                    t = progress.tasks[0].total
                    progress.update(task, completed=t or 1)

            success = downloader.download(
                url, format_spec, args.output, progress_hook
            )

        if success:
            ui.show_done(f"Saved to {args.output}")
        else:
            ui.show_error("Download failed. Check the URL or try with a different quality.")
            sys.exit(1)
    except KeyboardInterrupt:
        ui.console.print("\n[yellow]Interrupted by user.[/]")
        sys.exit(130)


if __name__ == '__main__':
    main()
