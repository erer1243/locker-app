# python stuff
import sys

# java stuff
import os
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64'
from jnius import autoclass
# get android bluetooth classes
BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
UUID = autoclass('java.util.UUID')

# kivy stuff
import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.lang import Builder


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stylesheet = '''
BoxLayout:
    id: box
    Label:
        text: "0"
        id: number
    Button:
        text: "Add 1 to label"
        on_release: app.addOneToLabel()
        '''
    def build(self):
        return Builder.load_string(self.stylesheet)

# when app is run directly
if __name__ == "__main__":
    try:
        app = MainApp()
    except:
        from errorpage import ErrorMain
        ErrorMain(str(sys.exc_info())).run()

    try:
        app.run()
    except:
        app.stop()
        from errorpage import ErrorMain
        ErrorMain(str(sys.exc_info())).run()
