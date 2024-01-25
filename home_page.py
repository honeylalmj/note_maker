from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel


KV = '''
FloatLayout:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1.0  # White background color (RGBA values)
        Rectangle:
            pos: self.pos
            size: self.size

    MDIcon:
        icon: "home"
        pos_hint: {"center_x": .5, "center_y": .7}
        font_size: "36sp"       
    MDRaisedButton:
        text: "Create"
        size_hint: 0.12, 0.08
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        md_bg_color: "green" 
        on_press: app.createnote()
  
    MDRaisedButton:
        text: "View"
        size_hint: 0.12, 0.08
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        md_bg_color: "green"
        on_press: app.view()  
    MDLabel:
        text: "Choose an action"
        size_hint: 0.4, 0.05
        pos_hint: {'center_x': 0.66, 'center_y': 0.4}
        theme_text_color: "Primary"
              

'''


class Home(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)

    def build(self):
        return self.screen
    
    def createnote(self):
        self.stop()
        from create import Create
        Create().run()

    def view(self):
        self.stop()
        from view_screen import ViewScreen
        ViewScreen().run()     


if __name__ == '__main__':
    Home().run()