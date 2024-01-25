from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
import json
from kivymd.uix.label import MDLabel
import os
import sys
KV = '''
BoxLayout:
    orientation: 'vertical'
    ScrollView:
        MDBoxLayout:
            id: container
            orientation: 'vertical'
    FloatLayout:
        size_hint_y: None
        height: dp(50)  # Adjust the height of the FloatLayout if needed
        pos_hint: {"center_x": 0.5, "top": 0.98}  # Adjust the "top" value as needed

        MDRaisedButton:
            text: 'Back'
            md_bg_color: "green"
            size_hint: 0.07, 0.06
            pos_hint: {"center_x": 0.4855, "center_y": 0.5}
            on_press: app.back()

'''

class Display(MDApp):
    def __init__(self,date, data,**kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        self.date = date
        self.datas = data
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(__file__)
        self.data_file_path = os.path.join(base_path,'data.json')

    def read_file(self):
        try:
            with open(self.data_file_path, 'r') as file:
                data = json.load(file)
                return data
        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            print("Data not found")
            return {}

    def build(self):
        self.root = Builder.load_string(KV)
        self.on_press()
        return self.root

    def back(self):
        self.root.ids.container.clear_widgets()
        self.stop()
        from view_screen import ViewScreen
        ViewScreen().run()

    def on_press(self):
        data = self.read_file()
        if self.date in data['Date']:
            date_data = data['Date'][self.date]
            for key, note_details in date_data.items():
                note_text = note_details.get('note', '')
                self.add_rich_label(f"{key}", f"{note_text}")
            print(f"Data for {self.date}: {date_data}")
        else:
            print(f"No data found for {self.date}")

    def add_rich_label(self, category, details):
        rich_label = MDLabel(
            text=f"[b]{category}[/b]: {details}",
            theme_text_color="Primary",
            markup=True
        )
        self.root.ids.container.add_widget(rich_label)

if __name__ == '__main__':
    Display().run()
