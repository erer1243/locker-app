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
# not to be used for catastrophic failure
def fail(reason, **kwargs):
    from failurepage import FailureScreen
    return FailureScreen(reason, **kwargs)

# display simple traceback page
# to be used in event of total failure
def error():
    from errorpage import ErrorMain
    ErrorMain(str(sys.exc_info())).run()

class ScreenDisplayController(ScreenManager):
    def handleBluetoothID(self):
        if not self.ids.id_entry_screen.ids.grid.ids.header.text:
            import time
            for _ in range(0, 5):
                self.ids.id_entry_screen.ids.grid.ids.header.text = "[color=#ff0000]Enter Locker Bluetooth ID[/color]"
                time.sleep(0.1)
                self.ids.id_entry_screen.ids.grid.ids.header.text = "Enter Locker Bluetooth ID"
class MainApp(App):
    def log(self, tag, message):
        log(tag, message)

    def checkForLocker(self, name):
        for device in self.paired_devices:
            log("mainapp.checkForLocker", str(device.getName()))

    def build(self):
        # get bluetooth default adapter
        # assumes device can use bluetooth!
        log("mainapp.build", "Getting bluetooth adapter")
        self.bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
        # enable bluetooth if not already
        if not self.bluetooth_adapter.isEnabled():
            log("mainapp.build", "Enabling bluetooth adapter")
            self.bluetooth_adapter.enable()
            # wait for state to be STATE_ON
            while(self.bluetooth_adapter.getState() != 12): # 12 is constant for STATE_ON
                pass
        # get paired devices from bluetoothadapter
        log("mainapp.build", "Getting paired devices")
        self.paired_devices = self.bluetooth_adapter.getBondedDevices().toArray()
        # if paired devices is empty
        if not self.paired_devices:
            log("mainapp.build", "No paired devices found, failing!")
            return fail("No paired Bluetooth devices! Please pair with the locker in the settings menu and restart the app.")
        log("mainapp.build", "Phone has paired devices")

        log("mainapp.build", "Loading first screen")
        return Builder.load_file('main.kv')

class AppManager():
    def __init__(self):
        try:
            self.app = MainApp()
        except:
            error()

        # try running the app, this is where it will most likely fail
        try:
            self.app.run()
        except SystemExit: # if sys.exit is called, allow it to finish and quit
            sys.exit()
        except: # otherwise stop the app and show error
            self.app.stop()
            error()

# when app is run directly
if __name__ == "__main__":
    AppManager()
