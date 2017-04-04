package tk.jealmas.plantgrowthcontroller.data;

import android.os.AsyncTask;
import android.util.Log;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;

public class ConfigTransmitter extends AsyncTask<Void, Void, Boolean> {

    private ConfigTransmitterListener configTransmitter;
    private String IP;

    public ConfigTransmitter(ConfigTransmitterListener configTransmitter, String IP) {
        this.configTransmitter = configTransmitter;
        this.IP = IP;
    }

    public interface ConfigTransmitterListener {
        void onSuccess();
        void onFail();
    }


    @Override
    protected Boolean doInBackground(Void... params) {
        byte[] message = {(byte)'1', (byte)'5', (byte)':', (byte)'0', (byte)'0',(byte)'\n'};
        try {
            Socket socket = new Socket(IP, 5001);
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
        } catch (Exception e) {
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
