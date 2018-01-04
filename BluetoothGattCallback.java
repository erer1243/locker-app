package lockerapp;

import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothGattService;
import android.util.Log;
import java.util.UUID;

class BTManager extends BluetoothGattCallback {
  // static constants
  private static final int STATE_DISCONNECTED = 0;
  private static final int STATE_CONNECTING = 1;
  private static final int STATE_CONNECTED = 2;
  private static final int STATE_DISCONNECTING = 3;
  // functional constants initialized later
  private BluetoothGattCharacteristic tx_char;
  private BluetoothGattCharacteristic rx_char;
  private UUID tx;
  private UUID rx;
  private UUID uart;
  // for keeping track of status between python and java
  private int connection_state = STATE_DISCONNECTED;
  private boolean ever_connected = false;
  private boolean uart_ready = false;
  //for passing information between callbacks
  private String written_value;

  public BTManager(UUID uart_uuid, UUID tx_uuid, UUID rx_uuid){
    log("BTManager", "Initialized CustomGattCallback");
    uart = uart_uuid;
    tx = tx_uuid;
    rx = rx_uuid;
  }

  @Override
  public void onConnectionStateChange(BluetoothGatt gatt, int status, int newState){
    log("onConnectionStateChange", "Status: " + Integer.toString(status) + " newState: " + Integer.toString(newState));
    switch(newState){
      case STATE_CONNECTED:
        onConnect(gatt);
        break;
      case STATE_DISCONNECTED:
        onDisconnect();
        break;
      default: break;
    }
  }

  @Override
  public void onCharacteristicWrite(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic, int status){
    if(characterisitc.getValue() != written_value){
      written_value = "__FAIL";
      gatt.abortReliableWrite();
    }
    else{
      gatt.executeReliableWrite();
    }
  }

  public void onServicesDiscovered(BluetoothGatt gatt, int status){
    log("onServicesDiscovered", "Service discovered. Status: " + Integer.toString(status));

    if(status == 0){
      log("onServicesDiscovered", "All services discovered, checking for uart service");

      if(gatt.getService(uart) != null){
        log("onServicesDiscovered", "Uart service found");
        BluetoothGattService uart_service = gatt.getService(uart);

        if(uart_service.getCharacteristic(tx) != null){
          log("onServicesDiscovered", "TX characteristic found. This is a compatible device.");
          tx_char = uart_service.getCharacteristic(tx);
          // rx_char = uart_service.getCharacteristic(rx);
          uart_ready = true;
        }
      }
    }
  }

  public void onConnect(BluetoothGatt gatt){
    log("onConnect", "Bluetooth connected, discovering services.");
    gatt.discoverServices();
    ever_connected = true;
    connection_state = STATE_CONNECTED;
  }

  public void onDisconnect(){
    log("onDisconnect", "Bluetooth device disconnected.");
    uart_ready = false;
    connection_state = STATE_DISCONNECTED;
  }

  public boolean send(BluetoothGatt gatt, String message){
    if(!gatt.beginReliableWrite()){
      return false;
    }
    written_value = message;
    tx_char.setValue(message);
    gatt.writeCharacteristic(tx_char);
    if(written_value == "__FAIL"){
      return false;
    }
    return true;
  }

  // general helper methods/macros here out
  public int getConnectionState(){
    return connection_state;
  }

  public boolean getEverConnected(){
    return ever_connected;
  }

  public boolean getUartStatus(){
    return uart_ready;
  }

  public void log(String tag, String message){
    Log.d("locker-controller.BluetoothGattCallback" + tag, message);
  }
}
