from kivy.uix.gridlayout import GridLayout
import sys

class FailureScreen(GridLayout):
    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.add_widget(Label(text=message, size_hint=(1, .9)))
        self.add_widget(Button(text="Exit", on_release=sys.exit))
