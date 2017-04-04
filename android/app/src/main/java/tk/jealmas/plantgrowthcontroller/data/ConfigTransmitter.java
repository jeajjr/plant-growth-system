package tk.jealmas.plantgrowthcontroller.data;

import android.os.AsyncTask;
import android.util.Log;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;

public class ConfigTransmitter extends AsyncTask<Void, Void, Boolean> {

    private ConfigTransmitterListener configTransmitter;
    public ConfigTransmitter(ConfigTransmitterListener configTransmitter) {
        this.configTransmitter = configTransmitter;
    }

    public interface ConfigTransmitterListener {
        void onSuccess();
        void onFail();
    }


    @Override
    protected Boolean doInBackground(Void... params) {
        byte[] message = {(byte)'1', (byte)'5', (byte)':', (byte)'0', (byte)'0',(byte)'\n'};
        try {
            Socket socket = new Socket("192.168.0.3", 5001);
            DataOutputStream dOut = new DataOutputStream(socket.getOutputStream());

            Log.d("ConfigTransmitter", "got connection");

            dOut.writeInt(0x04);
            dOut.writeInt(0x05);
            dOut.write(message);

            Log.d("ConfigTransmitter", "sent message");

            DataInputStream dIn = new DataInputStream(socket.getInputStream());
            byte ans = dIn.readByte();
            Log.d("ConfigTransmitter", "read " + ((int) ans));

            if (((int) ans) == 0)
                return true;

        } catch (IOException e) {
            Log.e("ConfigTransmitter", "exception", e);
        }

        return false;
    }

    @Override
    protected void onPostExecute(Boolean aBoolean) {
        if (aBoolean)
            configTransmitter.onSuccess();
        else
            configTransmitter.onFail();

    }

}
