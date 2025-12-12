from yt_dlp import YoutubeDL
import sys

output_dir = "./output/"


# Sample URLs:
# Playlist:
# https://music.youtube.com/playlist?list=OLAK5uy_mBj-sSPwi2H0fOlNpXgre7v-r73lUd6Zs
# Single Song in Playlist:
# https://music.youtube.com/watch?v=uZwFVZgAuFk&list=OLAK5uy_mBj-sSPwi2H0fOlNpXgre7v-r73lUd6Zs

song_url = sys.argv[1] if len(sys.argv) > 1 else input("Enter URL: ")

if "playlist?list=" in song_url:
    output_path = f"{output_dir}%(playlist)s/%(track_number)s - %(title)s.%(ext)s"
elif "watch" in song_url and "&list=" in song_url:
    # Remove playlist component from a watch URL
    song_url = song_url.split("&list=")[0]
    output_path = f"{output_dir}%(title)s.%(ext)s"

ydl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
    "outtmpl": output_path
}

with YoutubeDL(ydl_opts) as ydl:
    ydl.download([song_url])
