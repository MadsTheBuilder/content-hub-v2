import yt_dlp


def fetch_video(url: str, download: bool = False):
    """
    Fetches video metadata and optionally downloads the actual video file.
    Use download=False if you just want to rip the title, description, or transcript metadata!
    """
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'tmp_downloads/%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=download)

        return {
            "title": info_dict.get('title'),
            "description": info_dict.get('description'),
            "duration": info_dict.get('duration'),
            "upload_date": info_dict.get('upload_date'),
            "downloaded_file_path": ydl.prepare_filename(info_dict) if download else None,
        }
