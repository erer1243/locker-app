package lockerapp;

import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothGattDescriptor;
import android.bluetooth.BluetoothGattService;
import android.bluetooth.BluetoothProfile;
import android.util.Log;
import java.util.List;
import java.util.UUID;
import static java.lang.System.*;

class BTManager extends BluetoothGattCallback {
  private static final int STATE_DISCONNECTED = BluetoothProfile.STATE_DISCONNECTED;
  private static final int STATE_CONNECTED = BluetoothProfile.STATE_CONNECTED;

  private BluetoothGatt bt_gatt;
  private int connection_state;
  private boolean ever_connected = false;
  private UUID tx;
  private UUID rx;
  private UUID uart;

  public BTManager(UUID uart_uuid, UUID tx_uuid, UUID rx_uuid){
    log("CustomGattCallback", "Initialized CustomGattCallback");
    connection_state = STATE_DISCONNECTED;
    log("CustomGattCallback", "connection state set to 0, STATE_DISCONNECTED.");
    uart = uart_uuid;
    tx = tx_uuid;
    rx = rx_uuid;
  }

  @Override
  public void onConnectionStateChange(BluetoothGatt gatt, int status, int newState){
    log("onStateChange", "Status: " + Integer.toString(status) + " newState: " + Integer.toString(newState));

    if(newState == STATE_CONNECTED){
      log("onStateChange", "Bluetooth device initially connected!");
      log("onStateChange", "Discovering services");
      gatt.discoverServices();
      ever_connected = true;
      connection_state = STATE_CONNECTED;
    }

    if(newState == STATE_DISCONNECTED){
      log("onStateChange", "Bluetooth device disconnected!");
      connection_state = STATE_DISCONNECTED;
    }
  }

  public void onServicesDiscovered(BluetoothGatt gatt, int status){
    log("onServicesDiscovered", "Service discovered. Status: " + Integer.toString(status));
    if(status == 0){
      log("onServicesDiscovered", "All services discovered, checking for uart service");

      if(gatt.getService(uart) != null){
        log("onServicesDiscovered", "UART FOUND OOO");
        BluetoothGattService uart_service = gatt.getService(uart);
        if(uart_service.getCharacteristic(tx) != null){

          log("onServicesDiscovered", "TX characteristic found! This is a proper device.");
          BluetoothGattCharacteristic tx_char = uart_service.getCharacteristic(tx);
          BluetoothGattCharacteristic rx_char = uart_service.getCharacteristic(rx);

          tx_char.setValue("TEST!");
          gatt.writeCharacteristic(tx_char);
          log("onServicesDiscovered", "Test sent! Look for it on serial line");
        }
        else{
          log("onServicesDiscovered", "tx service not found :^(");
        }
      }
      else{
        log("onServicesDiscovered", "Uart not found :^(");
      }
    }
  }

  public int getConnectionState(){
    return connection_state;
  }

  public boolean getEverConnected(){
    return ever_connected;
  }

  // general helper methods/macros here out
  public void log(String tag, String message){
    Log.d("locker-controller.BluetoothGattCallback" + tag, message);
  }
}
