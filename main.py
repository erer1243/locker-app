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
    red = False
    def handleBluetoothID(self):
        # if input text with all spaces removed is empty
        if self.ids.idbox.text.replace(" ", "") == "":
            log("ScreenDisplayController.handleBluetoothID", "Bluetooth ID rejected")
            # change header colors to get user attention
            if self.red:
                self.ids.header.color = (1, 1, 1, 1)
            else:
                self.ids.header.color = (1, 0, 0, 1)
            self.red = not self.red

        else:
            log("ScreenDisplayController.handleBluetoothID", "Bluetooth ID accepted as " + self.ids.idbox.text)
            if App.get_running_app().checkForLocker(self.ids.idbox.text):
                log("ScreenDisplayController.handleBluetoothID", "Bluetooth ID is on the paired list")
            else:
                log("ScreenDisplayController.handleBluetoothID", "Bluetooth ID is not on the paired list, failing")


class MainApp(App):
    def log(self, tag, message):
        log(tag, message)

    def checkForLocker(self, name):
        for device in self.paired_devices:
            if device.getName() == name:
                return True
        return False

    def getBluetoothInfo(self):
        # enable bluetooth if not already
        if not self.bluetooth_adapter.isEnabled():
            log("MainApp.getBluetoothInfo", "Enabling bluetooth adapter")
            self.bluetooth_adapter.enable()
            # wait for state to be STATE_ON
            while(self.bluetooth_adapter.getState() != 12): # 12 is constant for STATE_ON
                pass
        # get paired devices from bluetoothadapter
        log("MainApp.getBluetoothInfo", "Getting paired devices")
        self.paired_devices = self.bluetooth_adapter.getBondedDevices().toArray()
        # if paired devices is empty
        if not self.paired_devices:
            log("MainApp.getBluetoothInfo", "No paired devices found, failing!")
            return False
        log("MainApp.getBluetoothInfo", "Phone has paired devices")
        return True

    def build(self):
        # get bluetooth default adapter
        # assumes device can use bluetooth!
        log("MainApp.build", "Getting bluetooth adapter")
        self.bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()

        if not self.getBluetoothInfo():
            return fail("No paired Bluetooth devices! Please pair with the locker in the settings menu and restart the app.")
        else:
            log("MainApp.build", "Loading first screen")
            return Builder.load_file('main.kv')

    def on_pause(self):
        log("MainApp.on_pause", "run")
        return True
    def on_start(self):
        log("MainApp.on_start", "run")
        return True
    def on_stop(self):
        log("MainApp.on_stop", "run")
        return True
    def on_resume(self):
        log("Mainapp.on_resume", "run")
        return True
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
