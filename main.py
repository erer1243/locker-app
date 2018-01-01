'''python stuff'''
import sys
from textwrap import wrap
from time import sleep

'''java stuff'''
import os
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64'
from jnius import autoclass
# get android bluetooth classes
BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
BluetoothGattCallback = autoclass('android.bluetooth.BluetoothGattCallback')
BluetoothGatt = autoclass('android.bluetooth.BluetoothGatt')
UUID = autoclass('java.util.UUID')
# log(String tag, String message) tag is an identifier, usually the class it's logging from
logd = autoclass('android.util.Log').d
def log(tag, message):
    logd("\nlocker-controller." + tag, message+'\n')

'''kivy stuff'''
import kivy
kivy.require('1.10.0')
# systems
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
# visual stuff
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
# display simple traceback page
# to be used in event of total failure
def error():
    from errorpage import ErrorMain
    msg = str(sys.exc_info())
    log("error", msg)
    ErrorMain(msg).run()

def popup(title, message):
    log("popup", "Showing popup for message: " + message)
    popup = Popup()
    popup.auto_close = False
    popup.size_hint = (None, None)
    popup.title = title

    text = wrap(message, 35)
    text = '\n'.join(text)
    label = Label(text=text, font_size=60)
    label.texture_update()

    pgrid = GridLayout()
    pgrid.rows = 2
    pgrid.cols = 1
    pgrid.add_widget(label)
    pgrid.add_widget(Button(text="Close", on_release=popup.dismiss, size_hint_y=.3))
    popup.size = (1000, label.texture_size[1]+400)
    popup.content = pgrid
    popup.open()

class ScreenDisplayController(ScreenManager):
    def __init__(self, firstpage, **kwargs):
        super().__init__(**kwargs)
        self.current = firstpage

    def bluetoothBasedDisplayManager(self):
        device_name = self.handleBluetoothID()              # get entered bluetooth ID if correct, else None
        log("ScreenDisplayController.bluetoothBasedDisplayManager", "device name passed from handler: " + str(device_name))
        if not device_name:                                 # if entered bluetooth ID is bad
            return                                              # do nothing
        app = App.get_running_app()

    def handleBluetoothID(self):
        App.get_running_app().startBluetoothAdapter()
        if self.ids['idbox'].text.replace(" ", "") == "":                              # if input box with spaces removed is empty
            log("ScreenDisplayController.handleBluetoothID", "Bluetooth ID blank")
            popup("Bluetooth ID Entry Error", "ID input is blank, please input a name.")

        else:                                                             # if Bluetooth id entry has a name input
            log("ScreenDisplayController.handleBluetoothID", "Checking paired list for " + self.ids.idbox.text)
            if App.get_running_app().checkForLocker(self.ids.idbox.text): # if that name is found
                log("ScreenDisplayController.handleBluetoothID", "Bluetooth ID is on the paired list")
                return self.ids.idbox.text

            else:                                                         # if that name is not found
                log("ScreenDisplayController.handleBluetoothID", "Bluetooth ID is not on the paired list, displaying message")
                popup("Bluetooth ID Entry Error", "Bluetooth device with ID " + self.ids.idbox.text + " is not paired with the phone.")

        return None

class MainApp(App):
    # get bluetooth default adapter
    # assumes device can use bluetooth!
    bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
    bluetooth_gatt_callback = BluetoothGattCallback()

    # UUIDString = "00001101-0000-1000-8000-00805F9B34FB" # generic primary access, not adafruit specific
    # UUIDString = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E" # generic uart from adafruit site
    UUIDString = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E" # TX uart from adafruit site
    # UUIDString = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E" # RX uart from adafruit site

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
        Builder.load_file('main.kv')

        if not self.getBluetoothInfo():
            log("MainApp.build", "Loading first screen no_paired_devices_failure")
            self.SDC = ScreenDisplayController("no_paired_devices_failure")
        else:
            log("MainApp.build", "Loading first screen name_entry")
            self.SDC = ScreenDisplayController("name_entry")
        return self.SDC

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
