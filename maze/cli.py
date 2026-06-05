import argparse
import sys

from . import downloader, ui


def main():
    try:
        parser = argparse.ArgumentParser(
            prog='mz',
            description='Maze - Universal Video Downloader',
            usage='mz <url> [options]',
        )
        parser.add_argument('url', help='Video URL (YouTube, Instagram, TikTok, etc.)')
        parser.add_argument('--mute', action='store_true', help='Download video without audio track')
        parser.add_argument('-o', '--output', default='.', help='Output directory (default: current)')

        args = parser.parse_args()

        ui.console.print("[bold yellow]Fetching video info...[/]")
        try:
            info = downloader.fetch_info(args.url)
        except Exception as e:
            ui.show_error(f"Could not fetch video: {e}")
            sys.exit(1)

        ui.show_header(info)

        if not info['resolutions']:
            ui.show_error("No video formats found. The video might be private or unavailable.")
            sys.exit(1)

        choice = ui.show_resolution_menu(info, mute=args.mute)
        if choice is None:
            ui.console.print("[yellow]Cancelled.[/]")
            sys.exit(0)

        resolutions = info['resolutions']
        resolution, mute, audio_only = ui.parse_choice(choice, resolutions, args.mute)
        format_spec = downloader.get_format_spec(resolution, mute, audio_only)

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
                args.url, format_spec, args.output, progress_hook
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
