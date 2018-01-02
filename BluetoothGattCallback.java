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
  private int connection_state;
  private UUID tx;
  private UUID rx;
  private UUID uart;

  //TODO onServicesDiscovered? 

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
      log("onStateChange", "Bluetooth device connected!");
      connection_state = STATE_CONNECTED;

      List<BluetoothGattService> service_list = gatt.getServices();
      BluetoothGattService services[] = service_list.toArray(new BluetoothGattService[service_list.size()]);

      //TODO print services
      log("onStateChange", "Services supported by device: ");
    }

    if(newState == STATE_DISCONNECTED){
      log("onStateChange", "Bluetooth device disconnected!");
      connection_state = STATE_DISCONNECTED;
    }
  }

  public int getConnectionState(){
    return connection_state;
  }

  // general helper methods/macros here out
  public void log(String tag, String message){
    Log.d("locker-controller.BluetoothGattCallback" + tag, message);
  }
}
