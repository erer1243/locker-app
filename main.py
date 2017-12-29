# python stuff
import sys

# java stuff
java = False # kivy on pc can't access android java classes, disable this to use on pc
if java:
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
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
class ScreenDisplayController(ScreenManager):
    pass
class MainMenu(Screen):
    pass
class OtherMenu(Screen):
    pass

class MainApp(App):
    def build(self):
        return Builder.load_file('main.kv')

# when app is run directly
if __name__ == "__main__":
    try:
        app = MainApp()
    except:
        print("section 1")
        from errorpage import ErrorMain
        ErrorMain(str(sys.exc_info())).run()

    try:
        app.run()
    except:
        print("section 2")
        app.stop()
        from errorpage import ErrorMain
        ErrorMain(str(sys.exc_info())).run()
