import socket
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup


class ChatApp(App):
    def build(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect(('127.0.0.1', 5555))  # Connect to the server
        except Exception as e:
            self.show_popup(f"Connection error: {str(e)}")
            return

        # Start a thread to handle receiving messages
        receiver_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receiver_thread.start()

        # Create the main layout
        self.layout = BoxLayout(orientation='vertical')

        # Scrollable area for chat history
        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.chat_log = Label(size_hint_y=None, text="Chat started!\n", markup=True)
        self.chat_log.bind(texture_size=self.chat_log.setter('size'))
        self.scroll.add_widget(self.chat_log)

        # Input area for sending messages
        self.message_input = TextInput(size_hint=(1, 0.1), multiline=False)
        self.message_input.bind(on_text_validate=self.send_message)

        # Send button
        send_button = Button(text="Send", size_hint=(1, 0.1))
        send_button.bind(on_press=self.send_message)

        # Add widgets to layout
        self.layout.add_widget(self.scroll)
        self.layout.add_widget(self.message_input)
        self.layout.add_widget(send_button)

        return self.layout

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message:
                    self.update_chat_log(f"[color=2980b9]received:[/color] {message}")
                else:
                    break
            except:
                break

    def send_message(self, _instance=None):
        message = self.message_input.text
        if message.lower() == 'exit':
            self.client.close()
            self.stop()
            return
        try:
            self.client.sendall(message.encode('utf-8'))
            self.update_chat_log(f"[color=27ae60]You:[/color] {message}")
            self.message_input.text = ""  # Clear input box
        except:
            self.show_popup("Failed to send message!")

    def update_chat_log(self, message):
        self.chat_log.text += message + "\n"
        self.scroll.scroll_y = 0  # Scroll to the bottom

    def show_popup(self, message):
        popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()


if _name_ == '_main_':
    ChatApp().run()
