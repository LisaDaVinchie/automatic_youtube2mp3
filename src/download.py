from yt_dlp import YoutubeDL
from pathlib import Path
# import sys


# Sample URLs:
# Playlist:
# https://music.youtube.com/playlist?list=OLAK5uy_mBj-sSPwi2H0fOlNpXgre7v-r73lUd6Zs
# Single Song in Playlist:
# https://music.youtube.com/watch?v=uZwFVZgAuFk&list=OLAK5uy_mBj-sSPwi2H0fOlNpXgre7v-r73lUd6Zs

class Downloader:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.url = ""

    def run(self, url: str):
        self.url = url
        output_path = self._create_output_path()
        ydl_opts = self._download_options(output_path)
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

    def _remove_playlist_component(self):
        if "watch" in self.url and "&list=" in self.url:
            self.url = self.url.split("&list=")[0]

    def _create_output_path(self) -> str:
        file_template = ""
        if "playlist?list=" in self.url:
            file_template = "%(playlist)s/%(track_number)s - %(title)s.%(ext)s"
            
        else:
            if "watch" in self.url and "&list=" in self.url:
                self._remove_playlist_component()
            
            file_template = "%(title)s.%(ext)s"
            
        return str(self.output_dir / file_template)

    def _download_options(self, output_path_template: Path = None, preferred_quality: int = 192, preferred_format: str = "mp3") -> dict:
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": preferred_format,
                "preferredquality": str(preferred_quality),
            }],
            "outtmpl": output_path_template
        }
        
        return ydl_opts

# if __name__ == "__main__":
#     downloader = Downloader(output_dir=Path("./output/"))
#     url = sys.argv[1] if len(sys.argv) > 1 else input("Enter URL: ")
    
#     # url = "https://music.youtube.com/watch?v=uZwFVZgAuFk&list=OLAK5uy_mBj-sSPwi2H0fOlNpXgre7v-r73lUd6Zs"
#     downloader.run(url)