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
BluetoothGattCallback = autoclass('android.bluetooth.BluetoothGattCallback')
UUID = autoclass('java.util.UUID')
# BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
# BluetoothGatt = autoclass('android.bluetooth.BluetoothGatt')

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
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
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

    def on_resume(self):
        log("ScreenDisplayController.on_resume", "Device resuming, re-attaining paired bluetooth devices")
        App.get_running_app().getBluetoothInfo()

    def bluetoothBasedDisplayManager(self, ID):
        name_good = self.handleBluetoothID(ID) # get entered bluetooth ID if correct, else None
        log("ScreenDisplayController.bluetoothBasedDisplayManager", "device name passed from handler: " + ID)
        if not name_good:                    # if entered bluetooth ID is bad
            return                                 # do nothing
        app = App.get_running_app()
        log("ScreenDisplayController.bluetoothBasedDisplayManager", "Trying to connect to device.")
        log("ScreenDisplayController.bluetoothBasedDisplayManager", str(app.connectToDevice()))

    def handleBluetoothID(self, ID):
        app = App.get_running_app()
        app.startBluetoothAdapter()
        if ID.replace(" ", "") == "":                 # if input box with spaces removed is empty
            log("ScreenDisplayController.handleBluetoothID", "Bluetooth ID blank")
            popup("Bluetooth ID Entry Error", "ID input is blank, please input a name.")

        else:                                                             # if Bluetooth id entry has a name input
            log("ScreenDisplayController.handleBluetoothID", "Checking paired list for " + ID)
            if app.checkForLocker(ID): # if that name is found
                log("ScreenDisplayController.handleBluetoothID", "Bluetooth ID is on the paired list")
                return True

            else:                                                         # if that name is not found
                log("ScreenDisplayController.handleBluetoothID", "Bluetooth ID is not on the paired list, displaying message")
                popup("Bluetooth ID Entry Error", "Bluetooth device with ID \"" + ID + "\" is not paired with the phone.")

        return False

class MainApp(App):
    # get bluetooth default adapter
    # assumes device can use bluetooth!
    bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
    bluetooth_gatt_callback = BluetoothGattCallback()

    # UUIDString = "00001101-0000-1000-8000-00805F9B34FB" # generic primary access, not adafruit specific
    uart_service_uuid = UUID.fromString("6E400001-B5A3-F393-E0A9-E50E24DCCA9E") # generic uart from adafruit site
    tx_uuid = UUID.fromString("6E400002-B5A3-F393-E0A9-E50E24DCCA9E") # TX uart from adafruit site
    rx_uuid = UUID.fromString("6E400003-B5A3-F393-E0A9-E50E24DCCA9E") # RX uart from adafruit site

    def connectToDevice(self):
        def fail():
            popup("Bluetooth Connection Error", "Could not connect to \'" + self.device.getName() + "\', make sure you are close enough to it and it is powered on.")
        # we're working without a callback class here
        # have to just time stuff and check if there's a connection
        log("MainApp.connectToDevice", "Trying to connect to device")
        gatt = self.device.connectGatt(None, True, self.bluetooth_gatt_callback)
        log("MainApp.connectToDevice", "Attempting to get uart service")
        connected = False
        for _ in range(0, 10):
            sleep(1)
            uart_service = gatt.getService(self.uart_service_uuid)
            if uart_service:
                log("MainApp.connectToDevice", "UART service found!")
                connected = True
                break
        if not connected:
            log("MainApp.connectToDevice", "UART service NOT found!")
            gatt.disconnect()
            fail()
            return False
        return True

    def checkForLocker(self, name):
        for device in self.paired_devices:
            if device.getName() == name:
                self.device = device
                log("MainApp.checkForLocker", "Device to be used set to " + str(device))
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

    def initBluetoothInfo(self):
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

    def getBluetoothInfo(self):
        def correctScreen(name):
            if not self.SDC.current == name:
                self.SDC.current = name
        self.startBluetoothAdapter()
        # get paired devices from bluetoothadapter
        log("MainApp.getBluetoothInfo", "Getting paired devices")
        self.paired_devices = self.bluetooth_adapter.getBondedDevices().toArray()
        # if paired devices is empty
        if not self.paired_devices:
            correctScreen("no_paired_devices_failure")
            log("MainApp.getBluetoothInfo", "No paired devices found, failing!")
            return False
        correctScreen("name_entry")
        log("MainApp.getBluetoothInfo", "Phone has paired devices")
        return True

    def build(self):
        Builder.load_file('main.kv')

        if not self.initBluetoothInfo():
            log("MainApp.build", "Loading first screen no_paired_devices_failure")
            self.SDC = ScreenDisplayController("no_paired_devices_failure")
        else:
            log("MainApp.build", "Loading first screen name_entry")
            self.SDC = ScreenDisplayController("name_entry")
        self.SDC.transition = NoTransition()
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
