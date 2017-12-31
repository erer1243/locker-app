# python stuff
import sys
from textwrap import wrap
from time import sleep

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
    def returnToNameEntry(self, btn):
        self.current = "name_entry"

    def bluetoothBasedDisplayManager(self):
        device_name = self.handleBluetoothID()              # get entered bluetooth ID if correct, else None
        log("ScreenDisplayController.bluetoothBasedDisplayManager", "device name passed from handler: " + device_name)
        if not device_name:                                 # if entered bluetooth ID is bad
            return                                              # do nothing
        app = App.get_running_app()
        log("DEBUG", "Creating bluetooth socket")
        socket = app.createLockerSocket(device_name)
        socket.connect()
        log("ScreenDisplayController.bluetoothBasedDisplayManager", "Got socket")
        log("ScreenDisplayController.bluetoothBasedDisplayManager", str(socket.isConnected()))
        rstream = socket.getInputStream()
        sstream = socket.getOutputStream()

        log("DEBUG", str(type(rstream)))
        log("DEBUG", str(type(sstream)))
        sstream.write("test :O\n")
        sstream.flush()

    header_red = False
    not_on_list_shown = False
    def handleBluetoothID(self):
        App.get_running_app().startBluetoothAdapter()
        if self.ids.idbox.text.replace(" ", "") == "":                              # if input box with spaces removed is empty
            log("ScreenDisplayController.handleBluetoothID", "Bluetooth ID blank")
            if self.header_red:                                                         # if header is currently red
                self.ids.header.color = (1, 1, 1, 1)                                        # set it to white
            else:                                                                       # if header is not red
                self.ids.header.color = (1, 0, 0, 1)                                        # set it to red
            self.header_red = not self.header_red                                       # record what color it is now

        else:                                                                                                   # if Bluetooth id entry has a name input
            log("ScreenDisplayController.handleBluetoothID", "Checking paired list for " + self.ids.idbox.text)
            if App.get_running_app().checkForLocker(self.ids.idbox.text):                                       # if that name is found
                log("ScreenDisplayController.handleBluetoothID", "Bluetooth ID is on the paired list")              # log it
                self.ids.header.color = (1, 1, 1, 1)                                                                # Set header color to white
                if self.not_on_list_shown:                                                                          # if the failure text is shown
                    self.ids.name_entry_grid.rows = 4                                                                   # remove it
                    self.not_on_list_shown = False                                                                      # .
                    self.ids.name_entry_grid.remove_widget(self.not_on_list)                                            # .
                return self.ids.idbox.text

            else:                                                                                               # if that name is not found
                if not self.not_on_list_shown:                                                                  # if failure text isn't shown
                    self.not_on_list_shown = True                                                                   # record that it is now showing
                    from kivy.uix.label import Label                                                                # import label class
                    self.ids.name_entry_grid.rows = 5                                                               # add extra row to gridmanager
                    failtext = '\"' + self.ids.idbox.text + '\" is not on the paired list'                          # make failtext with entered bluetooth ID
                    failtext = '\n'.join(wrap(failtext, 25))                                               # wrap that failtext to fit screen
                    self.not_on_list = Label(text=failtext, color=(1,0,0,1), font_size=100)                         # create a label from that failtext
                    self.ids.name_entry_grid.add_widget(self.not_on_list)                                           # add the failtext to screen

                else:                                                                                           # if the failuretext is already shown
                    failtext = '\"' + self.ids.idbox.text + '\" is not on the paired list'                      # make failtext with entered bluetooth ID
                    failtext = '\n'.join(wrap(failtext, 25))                                           # wrap the failtext to fit screen
                    self.not_on_list.text = failtext                                                            # change label to hold new failtext
                log("ScreenDisplayController.handleBluetoothID", "Bluetooth ID is not on the paired list, displaying message")
        return None

class MainApp(App):
    UUIDString = "00001101-0000-1000-8000-00805F9B34FB"

    def createLockerSocket(self, name):
        log("MainApp.createLockerSocket", "creating locker socket from name " + name)
        for device in self.paired_devices:
            log("MainApp.createLockerSocket", "Comparting " + name + " to " + device.getName())
            if device.getName() == name:
                log("MainApp.createLockerSocket", "it's a match!")
                socket = device.createRfcommSocketToServiceRecord(
                    UUID.fromString(self.UUIDString)
                )
                log("MainApp.createLockerSocket", str(type(socket)))
                return socket
        log("MainApp.createLockerSocket", "could not create socket")
        return None

    def checkForLocker(self, name):
        for device in self.paired_devices:
            if device.getName() == name:
                return True
        return False

    def startBluetoothAdapter(self):
        # enable bluetooth if not already
        if not self.bluetooth_adapter.isEnabled():
            log("MainApp.startBluetoothAdapter", "Enabling bluetooth adapter")
            self.bluetooth_adapter.enable()
        # wait for state to be STATE_ON
        while(self.bluetooth_adapter.getState() != 12): # 12 is constant for STATE_ON
            pass

    def getBluetoothInfo(self):
        self.startBluetoothAdapter()
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
