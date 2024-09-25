import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
import random
import string
from kivy.core.clipboard import Clipboard

kivy.require('2.0.0')  # Ensure you have the correct Kivy version

class PasswordGeneratorApp(App):

    def build(self):
        self.title = "Password Generator"
        layout = FloatLayout()

        # Background Image
        background = Image(source=r'C:\Users\ELCOT\PycharmProjects\pythonProject1\password.jfif', allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        layout.add_widget(background)

        # Main Layout for Widgets
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(None, None), size=(400, 500))
        main_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        layout.add_widget(main_layout)

        # Password Length Input
        self.length_label = Label(text="Password Length:", size_hint_y=None, height=40)
        self.length_input = TextInput(multiline=False, input_filter='int', size_hint_y=None, height=40)
        main_layout.add_widget(self.length_label)
        main_layout.add_widget(self.length_input)

        # Include Letters
        self.letters_switch = Switch(active=True)
        self.letters_label = Label(text="Include Letters", size_hint_y=None, height=40)
        letters_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        letters_layout.add_widget(self.letters_label)
        letters_layout.add_widget(self.letters_switch)
        main_layout.add_widget(letters_layout)

        # Include Numbers
        self.numbers_switch = Switch(active=True)
        self.numbers_label = Label(text="Include Numbers", size_hint_y=None, height=40)
        numbers_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        numbers_layout.add_widget(self.numbers_label)
        numbers_layout.add_widget(self.numbers_switch)
        main_layout.add_widget(numbers_layout)

        # Include Symbols
        self.symbols_switch = Switch(active=True)
        self.symbols_label = Label(text="Include Symbols", size_hint_y=None, height=40)
        symbols_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        symbols_layout.add_widget(self.symbols_label)
        symbols_layout.add_widget(self.symbols_switch)
        main_layout.add_widget(symbols_layout)

        # Generate Button
        generate_button = Button(text="Generate Password", size_hint_y=None, height=50)
        generate_button.bind(on_press=self.generate_password)
        main_layout.add_widget(generate_button)

        # Result Label
        self.result_label = Label(text="Generated Password will appear here", size_hint_y=None, height=40)
        main_layout.add_widget(self.result_label)

        return layout

    def generate_password(self, instance):
        try:
            length = int(self.length_input.text)
            if length < 1:
                raise ValueError("Password length must be at least 1")

            use_letters = self.letters_switch.active
            use_numbers = self.numbers_switch.active
            use_symbols = self.symbols_switch.active

            characters = ''
            if use_letters:
                characters += string.ascii_letters
            if use_numbers:
                characters += string.digits
            if use_symbols:
                characters += string.punctuation

            if not characters:
                raise ValueError("At least one character type must be selected")

            password = ''.join(random.choice(characters) for _ in range(length))
            self.result_label.text = f"Generated Password: {password}"

            # Copy to clipboard using Kivy's Clipboard class
            Clipboard.copy(password)

        except ValueError as e:
            self.show_error(str(e))

    def show_error(self, message):
        popup = Popup(title='Error',
                      content=Label(text=message),
                      size_hint=(None, None), size=(400, 200))
        popup.open()


if _name_ == '_main_':
    PasswordGeneratorApp().run()
