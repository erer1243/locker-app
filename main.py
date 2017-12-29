# python stuff
import sys

# java stuff
java = True # kivy on pc can't access android java classes, disable this to use on pc
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

def fail(reason, **kwargs):
    from failurepage import FailureScreen
    return FailureScreen(reason, **kwargs)

class ScreenDisplayController(ScreenManager):
    pass
class MainApp(App):
    def __init__(self, paired_devices,**kwargs):
        super().__init__(**kwargs)
        self.paired_devices = paired_devices # get paired devices passed below

    def build(self):
        if not self.paired_devices:
            return fail("No paired Bluetooth devices!\nPlease pair with the locker in the settings menu and restart the app.")

        return Builder.load_file('main.kv')

# when app is run directly
if __name__ == "__main__":
    paired_devices = []
    if java:
        paired_devices = BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
    try:
        app = MainApp(paired_devices)
    except:
        from errorpage import ErrorMain
        ErrorMain(str(sys.exc_info())).run()

    try:
        app.run()
    except SystemExit:
        sys.exit()
    except:
        app.stop()
        from errorpage import ErrorMain
        ErrorMain(str(sys.exc_info())).run()
