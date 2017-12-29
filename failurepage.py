import sys
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.app import App


class FailureScreen(GridLayout):
    message = ''
    def __init__(self, reason, **kwargs):
        super().__init__(**kwargs)
        message = reason

Builder.load_string('''
<FailureScreen>:
    rows: 2
    cols: 1
    Label:
        text: root.getFailureMessage()
    Button:
        text: "exit"
        on_release: sys.exit
        size_hint_y: .1
''')

if __name__ == "__main__":
    class FailureTest(App):
        def __init__(self, message, **kwargs):
            super().__init__(**kwargs)
            self.grid = FailureScreen(message)
        def build(self):
            return self.grid

    FailureTest("Generic error message. This appears only in debugging, you should never see this.").run()
