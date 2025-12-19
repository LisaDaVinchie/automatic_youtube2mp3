from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView

from pathlib import Path
from download import Downloader

class YT_downloader_app(App):
        
    def build(self):
        self.output_dir = Path("./output/")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        layout = BoxLayout(orientation='vertical')
        
        # create a label
        self.label = Label(font_size='24sp')
        self.reset_label(None)
        
        # Create the text input for URL
        self.text_input = TextInput(hint_text='Enter YouTube URL here', size_hint=(1, 0.2), focused=False, multiline=False)
        self.text_input.bind(on_text_validate=self.on_download_button_press)
        
        # Create the download button
        download_button = Button(text='Download', size_hint=(1, 0.2))
        download_button.bind(on_press=self.on_download_button_press)
        
        # Create the stop button
        stop_button = Button(text='Stop', size_hint=(1, 0.2))
        stop_button.bind(on_press=self.on_stop_button_press)
        
        choose_folder_btn = Button(text="Choose destination folder")
        choose_folder_btn.bind(on_press=lambda _: self.open_folder_chooser())
        layout.add_widget(choose_folder_btn)
        
        print(f"Output directory set to: {self.output_dir}")
        self.downloader = Downloader(output_dir=self.output_dir)

        
        layout.add_widget(self.label)
        layout.add_widget(self.text_input)
        layout.add_widget(download_button)
        layout.add_widget(stop_button)

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
        Clock.schedule_once(self.reset_text_input, 1)
        Clock.schedule_once(self.reset_label, 3)
        
    def on_stop_button_press(self, instance):
        self.downloader.download_stop()
        self.label.text = "Download stopped."
        Clock.schedule_once(self.reset_label, 3)
        
    def reset_label(self, dt):
        self.label.text = "YouTube to MP3 Downloader"
        
    def reset_text_input(self, dt):
        self.text_input.text = ""
    
    def select_folder(self, popup):
        if self.filechooser.selection:
            self.output_dir = Path(self.filechooser.selection[0])
            self.output_dir.mkdir(parents=True, exist_ok=True)
            self.label.text = f"Destination: {self.output_dir}"
        popup.dismiss()

        
    def open_folder_chooser(self):
        layout = BoxLayout(orientation='vertical')

        self.filechooser = FileChooserListView(
            path=str(Path.home()),
            dirselect=True
        )

        btn_layout = BoxLayout(size_hint_y=None, height=50)

        select_btn = Button(text="Select")
        cancel_btn = Button(text="Cancel")

        btn_layout.add_widget(select_btn)
        btn_layout.add_widget(cancel_btn)

        layout.add_widget(self.filechooser)
        layout.add_widget(btn_layout)

        popup = Popup(
            title="Select destination folder",
            content=layout,
            size_hint=(0.9, 0.9)
        )

        select_btn.bind(on_press=lambda _: self.select_folder(popup))
        cancel_btn.bind(on_press=popup.dismiss)

        popup.open()

if __name__ == '__main__':
    app = YT_downloader_app()
    app.run()