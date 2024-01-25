from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivy.uix.textinput import TextInput
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.dialog import MDDialog
import json
import os
import sys
KV = '''
FloatLayout:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1.0  # White background color (RGBA values)
        Rectangle:
            pos: self.pos
            size: self.size

    MDRaisedButton:
        id: date_button
        text: "Select Date"
        pos_hint: {'center_x': .5, 'center_y': .7}
        on_release: app.show_date_picker()
    MDIcon:
        icon: "calendar"
        pos_hint: {"center_x": .5, "center_y": .75}
        font_size: "36sp"
    MDIcon:
        icon: "pen"
        pos_hint: {"center_x": .255, "center_y": .6}
        font_size: "36sp"
    MDTextField:
        id: note_textfield
        multiline: True
        hint_text: "write your notes here"
        pos_hint: {"center_x": 0.5, "center_y": 0.45}
        size_hint: 0.5, 0.2 
    MDRaisedButton:
        text: "Save"
        md_bg_color: "green"
        pos_hint: {"center_x": 0.6, "center_y": 0.3}
        size_hint: 0.05, 0.05
        on_press: app.save()
    MDRaisedButton:
        text: "Back"
        md_bg_color: "green"
        pos_hint: {"center_x": 0.4, "center_y": 0.3}
        size_hint: 0.05, 0.05
        on_press: app.back()                    

'''


class Create(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        self.data = {}
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(__file__)
        self.data_file_path = os.path.join(base_path,'data.json')

    def build(self):
        return self.screen
    
    def save_data(self):
        try:
            with open(self.data_file_path, 'r') as file:
                exist_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            exist_data = {}

        date = self.data['Date']['Date']
        if 'Date' not in exist_data:
            exist_data['Date'] = {}

        if date not in exist_data['Date']:
            exist_data['Date'][date] = {}

        unique_key = 1
        while str(unique_key) in exist_data['Date'][date]:
            unique_key += 1

        exist_data['Date'][date][str(unique_key)] = {
            'Date': self.data['Date']['Date'],
            'note': self.data['Date']['note']
        }

        with open(self.data_file_path, 'w') as file:
            json.dump(exist_data, file, indent=2)

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
    def read_file(self):
        try:
            with open(self.data_file_path,'r')as file :
                data = json.load(file)
                return data
        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            print("Data not found")
            return {} 
          
    def on_save(self, instance, value, date_range):
        print(instance, value, date_range)
        self.screen.ids.date_button.text = f' {value.strftime("%d-%m-%Y")}'

    def on_cancel(self, instance, value):
        pass 
    def success_dialog(self):
        dialog = MDDialog(
            text="Your note saved successfully !",
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self.handle_verification_success_dialog_dismiss(dialog)
                )
            ]
        )
        dialog.open()

    def handle_verification_success_dialog_dismiss(self, dialog):
        dialog.dismiss()

        # Clear specific widgets
        self.screen.ids.note_textfield.text = ""
        self.screen.ids.date_button.text = "Select Date"

        # Clear error status and helper text if any
        self.screen.ids.note_textfield.error = False
        self.screen.ids.note_textfield.helper_text = ""
        self.screen.ids.date_button.error = False
        self.screen.ids.date_button.helper_text = ""

    def data_present_dialog(self, data, note_date):
        dialog = MDDialog(
            text="A Note already present for the same date! Do you want to continue?",
            buttons=[
                MDRaisedButton(
                    text="Yes",
                    on_release=lambda x: self.handle_continue(dialog, data, note_date),
                ),
                MDRaisedButton(
                    text='NO',
                    on_release=lambda x: self.handle_verification_success_dialog_dismiss(dialog),
                )
            ]
        )
        dialog.open()


    def handle_continue(self, dialog, data, note_date):
        dialog.dismiss()
        self.data['Date'] = data
        self.save_data()
        self.success_dialog()

        print(f"Note already present for {note_date}. Additional handling if needed.")

        self.screen.ids.note_textfield.text = ""
        self.screen.ids.date_button.text = "Select Date"

        self.screen.ids.note_textfield.error = False
        self.screen.ids.note_textfield.helper_text = ""
        self.screen.ids.date_button.error = False
        self.screen.ids.date_button.helper_text = ""

    def set_error_message(self, instance_textfield):

        if not instance_textfield.text.strip():
            instance_textfield.error = True
            instance_textfield.helper_text = "Required field"
        else:
            instance_textfield.error = False
            instance_textfield.helper_text = ""

    def save(self):
        note = self.screen.ids.note_textfield.text
        note_date = self.screen.ids.date_button.text
        present_data = self.read_file()

        self.screen.ids.note_textfield.error = False
        self.screen.ids.date_button.error = False

        if not note:
            self.screen.ids.note_textfield.error = True
            self.screen.ids.note_textfield.helper_text = "Required field"

        if note_date == "Select Date":
            self.screen.ids.date_button.error = True
            self.screen.ids.date_button.helper_text = "Required field"

        if note and (note_date != 'Select Date'):
            data = {
                'Date': note_date,
                'note': note}
            if note_date in present_data:
                self.data_present_dialog(data, note_date)
            else:
                self.data['Date'] = data
                self.save_data()
                self.success_dialog()
                print(self.data)
        
    def back(self):
        self.stop()
        from home_page import Home
        Home().run()


if __name__ == '__main__':
    Create().run()