'''
generic failsafe error page to simplify debugging on android
because adb logcat is terrible
'''
import kivy, sys
kivy.require('1.10.0')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.lang import Builder

Builder.load_string('''
<ErrorView>:
    Label:
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None
        text: root.text
''')
class ErrorView(ScrollView):
    text = StringProperty('')

class ErrorGrid(GridLayout):
    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 4
        self.add_widget(Label(text="The app has encountered an error! Traceback below.", size_hint=(1, .05)))
        self.add_widget(ErrorView(text=message.replace('\\n', '\n')))
        self.add_widget(Button(text="exit", on_release=sys.exit, size_hint=(1, .1)))

class ErrorMain(App):
    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)
        self.grid = ErrorGrid(message)
    def build(self):
        return self.grid

if __name__ == "__main__":
    ErrorMain("Generic error message. This appears only in debugging, you should never see this.").run()
