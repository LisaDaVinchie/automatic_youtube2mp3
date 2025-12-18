import unittest
from src.download import Downloader
from pathlib import Path
import shutil

class TestDownloader(unittest.TestCase):
    def setUp(self):
        self.output_dir = Path("./test_output/")
        self.downloader = Downloader(output_dir=self.output_dir)
        self.song_url = "https://music.youtube.com/watch?v=uZwFVZgAuFk&list=OLAK5uy_mBj-sSPwi2H0fOlNpXgre7v-r73lUd6Zs"
        self.playlist_url = "https://music.youtube.com/playlist?list=OLAK5uy_mBj-sSPwi2H0fOlNpXgre7v-r73lUd6Zs"

    def test_download_options(self):
        output_template = str(self.output_dir / "%(title)s.%(ext)s")
        preferred_quality = 256
        preferred_format = "wav"
        options = self.downloader._download_options(output_template, preferred_quality=preferred_quality, preferred_format=preferred_format)
        
        self.assertEqual(options["format"], "bestaudio/best")
        self.assertEqual(options["postprocessors"][0]["preferredcodec"], preferred_format)
        self.assertEqual(options["postprocessors"][0]["preferredquality"], str(preferred_quality))
        self.assertEqual(options["outtmpl"], output_template)
        self.assertTrue(options["quiet"])
        self.assertTrue(options["no_warnings"])
        
    def test_remove_playlist_component(self):
        original_url = "https://music.youtube.com/watch?v=uZwFVZgAuFk&list=OLAK5uy_mBj-sSPwi2H0fOlNpXgre7v-r73lUd6Zs"
        self.downloader.url = original_url
        self.downloader._remove_playlist_component()
        expected_url = "https://music.youtube.com/watch?v=uZwFVZgAuFk"
        self.assertEqual(self.downloader.url, expected_url)
        
    def test_create_output_path_song(self):
        self.downloader.url = self.song_url
        output_path = self.downloader._create_output_path()
        expected_template = str(self.output_dir / "%(title)s.%(ext)s")
        self.assertEqual(output_path, expected_template)
        
    def test_create_output_path_playlist(self):
        self.downloader.url = self.playlist_url
        output_path = self.downloader._create_output_path()
        expected_template = str(self.output_dir / "%(playlist)s/%(track_number)s - %(title)s.%(ext)s")
        self.assertEqual(output_path, expected_template)
        
    def test_run_song(self):
        # This test will only check if the run method executes without error.
        # Actual downloading is not performed in unit tests.
        try:
            self.downloader.download(self.song_url)
        except Exception as e:
            self.fail(f"Downloader.run() raised an exception unexpectedly: {e}")
            
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)