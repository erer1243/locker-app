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
kivy.require('1.10')
from kivy.app import App
from kivy.label import Label
from kivy.button import Button

class MainApp(App):
    def build(self):
        return Label(text="Hello!")

MainApp().run()
