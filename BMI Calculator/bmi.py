import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
import sqlite3

kivy.require('2.0.0')  # Ensure you have the correct Kivy version

class BMICalculatorApp(App):

    def build(self):
        layout = FloatLayout()

        # Background Image
        self.background = Image(source=r'C:\Users\ELCOT\PycharmProjects\pythonProject1\fitness.jfif ', allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        layout.add_widget(self.background)

        # Weight Input
        self.weight_label = Label(text="Weight (kg):", size_hint=(None, None), size=(150, 50),
                                  pos_hint={'x': 0.1, 'y': 0.7})
        self.weight_input = TextInput(multiline=False, input_filter='float', size_hint=(None, None), size=(150, 50),
                                      pos_hint={'x': 0.3, 'y': 0.7})

        # Height Input
        self.height_label = Label(text="Height (m):", size_hint=(None, None), size=(150, 50),
                                  pos_hint={'x': 0.1, 'y': 0.5})
        self.height_input = TextInput(multiline=False, input_filter='float', size_hint=(None, None), size=(150, 50),
                                      pos_hint={'x': 0.3, 'y': 0.5})

        # Calculate Button
        self.calculate_button = Button(text="Calculate BMI", size_hint=(None, None), size=(150, 50),
                                       pos_hint={'x': 0.1, 'y': 0.3}, background_color=(1, 0.5, 0, 1))
        self.calculate_button.bind(on_press=self.calculate_bmi)

        # Result Label
        self.result_label = Label(text="", size_hint=(None, None), size=(300, 50), pos_hint={'x': 0.1, 'y': 0.2})

        # Add widgets to layout
        layout.add_widget(self.weight_label)
        layout.add_widget(self.weight_input)
        layout.add_widget(self.height_label)
        layout.add_widget(self.height_input)
        layout.add_widget(self.calculate_button)
        layout.add_widget(self.result_label)

        # Initialize the database
        self.init_db()

        return layout

    def init_db(self):
        # Connect to SQLite database
        self.conn = sqlite3.connect('bmi_data.db')
        self.cursor = self.conn.cursor()
        # Create table if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bmi_data
                            (weight REAL, height REAL)''')
        self.conn.commit()

    def save_to_db(self, weight, height):
        self.cursor.execute('INSERT INTO bmi_data (weight, height) VALUES (?, ?)', (weight, height))
        self.conn.commit()

    def retrieve_last_valid_input(self):
        self.cursor.execute('SELECT weight, height FROM bmi_data ORDER BY ROWID DESC LIMIT 1')
        result = self.cursor.fetchone()
        if result:
            return result
        return None, None

    def calculate_bmi(self, instance):
        try:
            weight = float(self.weight_input.text)
            height = float(self.height_input.text)

            if weight <= 0 or height <= 0:
                # Retrieve last valid input if current inputs are invalid
                weight, height = self.retrieve_last_valid_input()

                if weight is None or height is None:
                    self.show_error("Weight and height must be positive numbers and there are no previous valid inputs.")
                    return

                self.show_error("Invalid input. Using last valid inputs for calculation.")

            else:
                # Save valid input to database
                self.save_to_db(weight, height)

            bmi = weight / (height ** 2)
            category = self.classify_bmi(bmi)

            self.result_label.text = f"Your BMI is {bmi:.2f}. Category: {category}"

        except ValueError:
            self.show_error("Please enter valid numbers for weight and height.")

    def classify_bmi(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

    def show_error(self, message):
        popup = Popup(title='Error',
                      content=Label(text=message),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

if _name_ == '_main_':
    BMICalculatorApp().run()
