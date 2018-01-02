package lockerapp;

import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothGattDescriptor;
import android.bluetooth.BluetoothGattService;
import android.util.Log;
import static java.lang.System.*;

class CustomGattCallback extends BluetoothGattCallback {
  private static final int STATE_DISCONNECTED = 0;
  private static final int STATE_CONNECTED = 1;
  private int connection_state;

  public CustomGattCallback(){
    log("CustomGattCallback", "Initialized CustomGattCallback");
    connection_state = STATE_DISCONNECTED;
    log("CustomGattCallback", "connection state set to 0, STATE_DISCONNECTED.");
  }

  @Override
  public void onConnectionStateChange(BluetoothGatt gatt, int status, int newState){
    log("onStateChange", "Status: " + str(status) + " newState: " + str(newState));
  }

  // helper methods/macros here out
  public void log(String tag, String message){
    Log.d("locker-controller.BluetoothGattCallback" + tag, message);
  }

  public String str(int input){
    return Integer.toString(input);
  }
}
