import os
import subprocess

import yt_dlp


class _NullLogger:
    def debug(self, msg): pass
    def info(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass

STANDARD_RES = [144, 240, 360, 480, 540, 720, 1080, 1440, 2160, 4320]
RES_LABELS = {
    144: '144p', 240: '240p', 360: '360p', 480: '480p', 540: '540p',
    720: '720p', 1080: '1080p', 1440: '2K', 2160: '4K', 4320: '8K',
}


def _round_to_std(height: int) -> int:
    return min(STANDARD_RES, key=lambda x: abs(x - height))


def _has_ffmpeg() -> bool:
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def fetch_info(url: str) -> dict:
    ydl_opts = {'quiet': True, 'no_warnings': True, 'logger': _NullLogger()}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    raw_formats = info.get('formats', [])
    heights = set()
    has_audio = False

    for f in raw_formats:
        vcodec = f.get('vcodec', 'none')
        acodec = f.get('acodec', 'none')
        if vcodec != 'none':
            h = f.get('height')
            if h:
                heights.add(_round_to_std(h))
        if acodec != 'none':
            has_audio = True

    site_key = info.get('extractor_key', 'Unknown')

    return {
        'title': info.get('title', 'Unknown'),
        'duration': info.get('duration'),
        'webpage_url': info.get('webpage_url', url),
        'extractor': site_key,
        'resolutions': sorted(heights),
        'has_audio': has_audio,
    }


def get_format_spec(resolution=None, mute=False, audio_only=False, has_ffmpeg=False):
    if audio_only:
        return 'bestaudio/best'
    if resolution is None:
        if mute:
            return 'bestvideo[vcodec!=?av01]/bestvideo/best'
        if has_ffmpeg:
            return 'bestvideo+bestaudio/best'
        return 'best'
    if mute:
        return f'bestvideo[height<={resolution}][vcodec!=?av01]/bestvideo[height<={resolution}]'
    if has_ffmpeg:
        return f'bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]'
    return f'best[height<={resolution}]'


def download(url, format_spec, output_dir='.', progress_hook=None):
    has_ffmpeg = _has_ffmpeg()
    outtmpl = os.path.join(os.path.abspath(output_dir), '%(title)s.%(ext)s')

    ydl_opts = {
        'format': format_spec,
        'outtmpl': outtmpl,
        'quiet': True,
        'no_warnings': True,
        'logger': _NullLogger(),
        'progress_hooks': [progress_hook] if progress_hook else [],
        'concurrent_fragment_downloads': 5,
    }

    if has_ffmpeg and '+' in format_spec:
        ydl_opts['merge_output_format'] = 'mp4'
        ydl_opts['postprocessor_args'] = {'ffmpeg': ['-c:a', 'aac', '-c:v', 'copy']}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ret = ydl.download([url])
            return ret == 0
    except Exception:
        # Retry sequentially if concurrent fragments gave 416
        ydl_opts['concurrent_fragment_downloads'] = 1
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ret = ydl.download([url])
                return ret == 0
        except Exception:
            return False
