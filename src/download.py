from yt_dlp import YoutubeDL
from pathlib import Path
import threading
# import time


# Sample URLs:
# Playlist:
# https://music.youtube.com/playlist?list=OLAK5uy_mBj-sSPwi2H0fOlNpXgre7v-r73lUd6Zs
# Single Song in Playlist:
# https://music.youtube.com/watch?v=uZwFVZgAuFk&list=OLAK5uy_mBj-sSPwi2H0fOlNpXgre7v-r73lUd6Zs

class Downloader:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.url = ""
        
        self.stop_download = False
        self.thread = None

    def download_start(self, url: str):
        self.stop_download = False
        
        self.thread = threading.Thread(
            target=self._run,
            args=(url,),
            daemon=True
            )
        
        self.thread.start()
        
    def download_stop(self):
        self.stop_download = True
        
    def _progress_hook(self, d):
        if self.stop_download:
            raise KeyboardInterrupt()

    def _run(self, url):
        self.url = url
        output_path = self._create_output_path()
        ydl_opts = self._download_options(output_path)
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])
            
    def is_valid_url(self, url: str) -> bool:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "logger": SilentLogger()
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(url, download=False)
            return True
        except Exception:
            return False


    def _create_output_path(self) -> str:
        file_template = ""
        if "watch" in self.url and "&list=" in self.url:
                self._remove_playlist_component()
                
        if "playlist?list=" in self.url:
            file_template = "%(playlist)s/%(track_number)s - %(title)s.%(ext)s"
        else:
            file_template = "%(title)s.%(ext)s"
            
        return str(self.output_dir / file_template)
    
    def _remove_playlist_component(self):
        if "watch" in self.url and "&list=" in self.url:
            self.url = self.url.split("&list=")[0]


    def _download_options(self, output_path_template: str, preferred_quality: int = 192, preferred_format: str = "mp3") -> dict:
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": preferred_format,
                "preferredquality": str(preferred_quality),
            }],
            "outtmpl": output_path_template,
            "quiet": True,
            "no_warnings": True,
            "progress_hooks": [self._progress_hook],
        }
        
        return ydl_opts
    
class SilentLogger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass
