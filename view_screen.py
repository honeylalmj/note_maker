from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
import json
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from datetime import datetime
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivy.uix.widget import Widget
import os
import sys
KV = '''
BoxLayout:
    orientation: 'vertical'
    ScrollView:
        MDBoxLayout:
            id: container
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            spacing: "20dp"  # Adjust the spacing between buttons if needed
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
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

class ViewScreen(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
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
    def on_start(self):
        data = self.read_file()
        if not data.get('Date', {}):
            self.empty_dialog()
    def build(self):
        self.root = Builder.load_string(KV)
        self.display_dates()
        return self.root

    def back(self):
        self.root.ids.container.clear_widgets()
        self.stop()
        from home_page import Home
        Home().run()

    def display_dates(self):
        data =self.read_file()
        self.root.ids.container.clear_widgets()
        padding_widget = Widget(size_hint_y=None, height=50)
        self.root.ids.container.add_widget(padding_widget)
        dates = data.get('Date', {})
        sorted_dates = sorted(dates.keys(), key=lambda x: datetime.strptime(x.strip(), '%d-%m-%Y'))
        for date in sorted_dates:
            self.add_button(date)
        top_position = 0.9  
        box_layout = MDBoxLayout(
            id='container',
            orientation='vertical',
            size_hint_y=None,
            height=self.root.ids.container.minimum_height,
            spacing="20dp",
            pos_hint={"center_x": 0.5, "top": top_position}
        )
        self.root.ids.container.add_widget(box_layout)
    def empty_dialog(self):
        dialog = MDDialog(
            text="The note list is empty !",
            buttons=[
                MDRaisedButton(
                    text="Ok",
                    on_release=lambda x: self.home_page_dialog(dialog)
                )

            ]
        )
        dialog.open()
    
    def home_page_dialog(self,dialog):
        dialog.dismiss()
        from home_page import Home
        Home().run()

    def add_button(self, text):
        box_layout = MDBoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=40,
        spacing=20,
        pos_hint={"center_x": 0.95}
    )
        
        # Date button
        button = MDRaisedButton(text=text, theme_text_color="Primary", font_style='Body1')
        button.bind(on_press=self.on_button_press)
        box_layout.add_widget(button)

        # Delete icon button
        delete_button = MDIconButton(icon="delete", theme_text_color="Primary")
        delete_button.bind(on_press=lambda x: self.delete_dialog(text))
        box_layout.add_widget(delete_button)

        self.root.ids.container.add_widget(box_layout)

    def delete_button_press(self,dialog,date):
        data = self.read_file()
        if date in data['Date']:
            del data['Date'][date]
            print(f"Date {date} removed successfully")
            # Write the updated data back to the JSON file
            with open(self.data_file_path, 'w') as file:
                json.dump(data, file, indent=2)
                print("Data written back to the file")
        else:
            print(f"Date {date} not found in the data")
        dialog.dismiss()
        self.display_dates()

    def delete_dialog(self,delete_date):
        date = str(delete_date)
        dialog = MDDialog(
            text=f"Do you really want to delete the note of {date}?",
            buttons=[
                MDRaisedButton(
                    text="YES",
                    on_release=lambda x: self.delete_button_press(dialog,delete_date)
                ),
                MDRaisedButton(
                    text="NO",
                    on_release=lambda x: self.dialog_dismiss(dialog)
                )
            ]
        )
        dialog.open()
    def dialog_dismiss(self,dialog):
        dialog.dismiss()

    def on_button_press(self, instance):
        data = self.read_file()
        self.stop()
        self.root.ids.container.clear_widgets()
        selected_date = instance.text
        data_for_selected_date = data.get('Date', {}).get(selected_date, {})
        from display import Display
        Display(selected_date,data_for_selected_date).run()
    

if __name__ == '__main__':
    ViewScreen().run()