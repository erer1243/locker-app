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
    Label:
        text: "hello"
        

        '''
    def build(self):
        return Builder.load_string(self.stylesheet)

# when app is run directly
if __name__ == "__main__":
    try:
        MainApp().run()
    except:
        from errorpage import ErrorMain
        ErrorMain(str(sys.exc_info())).run()
