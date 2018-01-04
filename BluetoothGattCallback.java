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
  private boolean last_write_status = false;

  public BTManager(UUID uart_uuid, UUID tx_uuid, UUID rx_uuid){
    log("BTManager", "Initialized BTManager");
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
    log("onCharacteristicWrite", "Status: " + Integer.toString(status));
    if(status == 0){
      log("onCharacteristicWrite", "Successful write.");
      last_write_status = true;
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

  // general helper methods/macros here out
  public BluetoothGattCharacteristic getTX(){
    return tx_char;
  }

  public boolean messageSentCorrectly(){
    return last_write_status;
  }

  public void resetWriteStatus(){
    last_write_status = false;
  }

  public int getConnectionState(){
    return connection_state;
  }

  public boolean getEverConnected(){
    return ever_connected;
  }

  // this is necessary because doing setvalue through pyjnius defaults argument type to byte[]
  public void setTXValue(String val){
    tx_char.setValue(val);
  }

  public boolean getUartStatus(){
    return uart_ready;
  }

  public void log(String tag, String message){
    Log.d("locker-controller.BTManager." + tag, message);
  }
}
