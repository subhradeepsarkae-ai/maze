from typing import Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    ProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)
from rich.text import Text
from rich.prompt import Prompt
from rich.align import Align

from .downloader import RES_LABELS

console = Console()

_peak_speed = [0.0]  # mutable for closure

def _fmt_speed(bytes_per_sec):
    if bytes_per_sec is None:
        return "--.- MB/s"
    mb = bytes_per_sec / 1_048_576
    if mb >= 1:
        return f"{mb:.1f} MB/s"
    return f"{bytes_per_sec / 1024:.0f} KB/s"


class SpeedMeterColumn(ProgressColumn):
    min_width = 12

    def render(self, task):
        speed = task.speed
        if speed is None:
            return Text("--.- MB/s", style="dim")
        _peak_speed[0] = max(_peak_speed[0], speed)
        mb_s = speed / 1_048_576
        if mb_s >= 10:
            style = "bold green"
        elif mb_s >= 3:
            style = "bold yellow"
        elif mb_s >= 1:
            style = "bold cyan"
        else:
            style = "bold red"
        return Text(f"{mb_s:.1f} MB/s", style=style)


def _format_duration(seconds: Optional[int]) -> str:
    if not seconds:
        return '--:--'
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h:
        return f'{h}:{m:02d}:{s:02d}'
    return f'{m}:{s:02d}'


def _truncate(text: str, max_len: int = 50) -> str:
    if len(text) > max_len:
        return text[: max_len - 3] + '...'
    return text


def show_header(info: dict):
    source = info.get('extractor', 'Unknown')
    title_panel = Panel(
        f"[bold white]{_truncate(info['title'], 55)}[/]\n"
        f"[dim]{source}  |  {_format_duration(info['duration'])}[/]",
        border_style="blue",
    )
    header = Panel.fit(
        Align.center(
            "[bold yellow]Maze[/] [white]v1.0[/]   [cyan]Universal Video Downloader[/]"
        ),
        border_style="yellow",
    )
    console.print(header)
    console.print(title_panel)


def show_resolution_menu(info: dict, mute: bool = False) -> Optional[int]:
    resolutions = info['resolutions']

    table = Table(show_header=True, header_style="bold cyan", border_style="blue")
    table.add_column("#", style="dim", width=3)
    table.add_column("Quality", width=14)
    table.add_column("Info", width=18)

    for i, res in enumerate(resolutions, 1):
        label = RES_LABELS.get(res, f'{res}p')
        info_text = "Video only" if mute else "Video + Audio"
        table.add_row(str(i), f"[bold]{label}[/]", info_text)

    i = len(resolutions) + 1
    table.add_row(
        str(i),
        "[bold green]Best Available[/]",
        "Video only" if mute else "Video + Audio",
    )

    if not mute:
        i += 1
        table.add_row(str(i), "[bold magenta]Audio Only[/]", "MP3 / M4A")

    console.print(table)

    max_choice = len(resolutions) + (2 if not mute else 1)
    while True:
        choice = Prompt.ask(
            f"\n[bold yellow]>[/] Pick quality [dim](1-{max_choice}, q to quit)[/]",
            default=None,
        )
        if choice and choice.lower() in ('q', 'quit', 'exit'):
            return None
        try:
            num = int(choice)
            if 1 <= num <= max_choice:
                return num
        except (ValueError, TypeError):
            pass
        console.print("[red]Invalid choice. Try again.[/]")


def parse_choice(choice: int, resolutions: list, mute: bool) -> tuple:
    if mute:
        if choice <= len(resolutions):
            return (resolutions[choice - 1], True, False)
        return (None, True, False)

    if choice <= len(resolutions):
        return (resolutions[choice - 1], False, False)
    if choice == len(resolutions) + 1:
        return (None, False, False)
    return (None, False, True)


def create_progress() -> Progress:
    return Progress(
        TextColumn("[bold blue]{task.fields[name]}"),
        BarColumn(bar_width=40),
        "[progress.percentage]{task.percentage:>3.1f}%",
        "|",
        DownloadColumn(),
        "|",
        SpeedMeterColumn(),
        "|",
        TimeRemainingColumn(),
        console=console,
    )


def reset_peak():
    _peak_speed[0] = 0.0


def show_done(message: str = "Download complete!"):
    if _peak_speed[0]:
        message += f" [dim](peak: {_fmt_speed(_peak_speed[0])})[/]"
    console.print(f"\n[bold green]OK[/] {message}")


def show_error(message: str):
    console.print(f"\n[bold red]Error:[/] {message}")
