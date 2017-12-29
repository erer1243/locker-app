import kivy, sys
kivy.require('1.10.0')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout

class ErrorGrid(GridLayout):
    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 3
        self.add_widget(Label(text="The app has encountered an error! Traceback below.", size_hint=(1, .1)))
        self.add_widget(TextInput(text=message))
        self.add_widget(Button(text="exit", on_release=sys.exit, size_hint=(1, .1)))

class ErrorMain(App):
    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)
        self.grid = ErrorGrid(message)
    def build(self):
        return self.grid

if __name__ == "__main__":
    ErrorMain("Generic error message. This appears only in debugging, you should never see this.").run()
