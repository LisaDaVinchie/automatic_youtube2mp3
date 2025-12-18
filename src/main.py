from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

from pathlib import Path

from download import Downloader

class YT_downloader_app(App):
        
    def build(self):
        self.output_dir = Path("./output/")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.downloader = Downloader(output_dir=self.output_dir)
        layout = BoxLayout(orientation='vertical')
        # create a label
        self.label = Label(text='YouTube to MP3 Downloader', font_size='24sp')
        
        # Create the text input for URL
        self.text_input = TextInput(hint_text='Enter YouTube URL here', size_hint=(1, 0.2), focused=False, multiline=False)
        self.text_input.bind(on_text_validate=self.on_download_button_press)
        
        # Create the download button
        download_button = Button(text='Download', size_hint=(1, 0.2))
        download_button.bind(on_press=self.on_download_button_press)
        
        layout.add_widget(self.label)
        layout.add_widget(self.text_input)
        layout.add_widget(download_button)

        return layout
    
    def on_download_button_press(self, instance):
        self.url = self.text_input.text
        if not self.url:
            self.label.text = "Please enter a URL first."
            return
        
        if not self.downloader.is_valid_url(self.url):
            self.label.text = "Invalid URL. Please enter a valid YouTube or YoutubeMusic URL."
            return
        
        self.label.text = "Downloading..."
        self.downloader.download_start(self.url)
        self.label.text = f"Download complete, file saved to {self.output_dir}"

if __name__ == '__main__':
    app = YT_downloader_app()
    app.run()