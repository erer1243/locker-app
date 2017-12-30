import sys, textwrap
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class FailureScreen(GridLayout):
    def __init__(self, error, **kwargs):
        super().__init__(**kwargs)
        self.rows = 2
        self.cols = 1
        self.error = "\n".join(textwrap.wrap(error, 29))
        self.add_widget(Label(text=self.error, font_size=80))
        self.add_widget(Button(text="exit", on_release=sys.exit, size_hint_y=.1))

if __name__ == "__main__":
    from kivy.app import App
    class FailureTest(App):
        def build(self):
            return FailureScreen("OH NO GENERIC ERRORRRRR!!!")

    FailureTest().run()
