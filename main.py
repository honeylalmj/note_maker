from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from home_page import Home

KV = '''
FloatLayout:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1.0  # White background color (RGBA values)
        Rectangle:
            pos: self.pos
            size: self.size
    MDRaisedButton:
        text: "WRITE YOUR NOTE"
        size_hint: 0.3, 0.1
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        md_bg_color: "blue"   
    MDRaisedButton:
        text: "Lets start writing..."
        size_hint: 0.2, 0.1
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        md_bg_color: "green"
        on_press: app.proceed()  

'''


class Start(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)

    def build(self):
        return self.screen
    
    def proceed(self):
        self.stop()
        Home().run()

if __name__ == '__main__':
    Start().run()