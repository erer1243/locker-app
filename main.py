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
log = autoclass('android.util.Log').d

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
    def build(self):
        # assumes device can use bluetooth!
        self.bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
        log("mainapp.build", "Getting bluetooth adapter!")


        # if paired devices is empty
        if not self.paired_devices:
            log("mainapp.build", "No paired devices found, failurepage.py")
            return fail("No paired Bluetooth devices! Please pair with the locker in the settings menu and restart the app.")

        for device in self.paired_devices:
            print(device)

        return Builder.load_file('main.kv')


def restartApp(instance=None):
    if instance:
        instance.stop()

    try:
        app = MainApp()
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

# when app is run directly
if __name__ == "__main__":
    restartApp()
