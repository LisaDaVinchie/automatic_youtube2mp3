from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class YT_downloader_app(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        # create a label
        self.label = Label(text='YouTube to MP3 Downloader', font_size='24sp')
        
        # create a button
        button = Button(text='Download', size_hint=(1, 0.2))
        button.bind(on_press=self.on_button_press)
        
        layout.add_widget(self.label)
        layout.add_widget(button)
        return layout
    
    def on_button_press(self, instance):
        self.label.text = "Download started..."
    
app = YT_downloader_app()

if __name__ == '__main__':
    app.run()