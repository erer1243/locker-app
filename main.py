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
# log(String tag, String message) tag is an identifier, usually the class it's logging from
logd = autoclass('android.util.Log').d
def log(tag, message):
    logd("\nlocker-controller." + tag, message+'\n')

# kivy stuff
import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# display simple failure page
def fail(reason, **kwargs):
    from failurepage import FailureScreen
    return FailureScreen(reason, **kwargs)

class ScreenDisplayController(ScreenManager):
    pass
class MainApp(App):
    def checkForLocker(self, name):
        for device in self.paired_devices:
            log("mainapp.checkForLocker", str(device))

    def build(self):
        log("mainapp.build", "Doing bluetoothAdapter things")
        # get bluetooth default adapter
        # assumes device can use bluetooth!
        self.bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
        # attempt to enable bluetooth
        self.bluetooth_adapter.enable()
        # get paired devices from bluetoothadapter
        self.paired_devices = self.bluetooth_adapter.getBondedDevices().toArray()

        # if paired devices is empty
        if not self.paired_devices:
            log("mainapp.build", "No paired devices found, failing!")
            return fail("No paired Bluetooth devices! Please pair with the locker in the settings menu and restart the app.")

        return Builder.load_file('main.kv')

class AppManager():
    def __init__(self):
        try:
            self.app = MainApp()
        except:
            from errorpage import ErrorMain
            ErrorMain(str(sys.exc_info())).run()
        # try running the app, where it will most likely fail
        try:
            self.app.run()
        except SystemExit: # if sys.exit is called, allow it to finish and quit
            sys.exit()
        except: # otherwise stop the app and show error
            self.app.stop()
            from errorpage import ErrorMain
            ErrorMain(str(sys.exc_info())).run()

# when app is run directly
if __name__ == "__main__":
    AppManager()
