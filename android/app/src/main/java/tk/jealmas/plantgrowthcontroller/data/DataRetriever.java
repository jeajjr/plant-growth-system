package tk.jealmas.plantgrowthcontroller.data;

import android.os.AsyncTask;
import android.util.Log;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;


public class DataRetriever extends AsyncTask<Void, Void, String> {

    private DataListener dataListener;

    public DataRetriever(DataListener dataListener) {
        this.dataListener = dataListener;
    }

    @Override
    protected String doInBackground(Void... params) {
        String jsonString = null;

        try {
            HttpURLConnection urlConnection = null;

            URL url = new URL("http://data.sparkfun.com/output/NJWqvnJNAyT0dNWZxrDd.json");

            urlConnection = (HttpURLConnection) url.openConnection();

            urlConnection.setRequestMethod("GET");
            urlConnection.setReadTimeout(10000 /* milliseconds */);
            urlConnection.setConnectTimeout(15000 /* milliseconds */);

            urlConnection.setDoInput(true);
            urlConnection.setDoOutput(true);

            urlConnection.connect();

            BufferedReader br = new BufferedReader(new InputStreamReader(url.openStream()));

            char[] buffer = new char[1024];

            jsonString = new String();

            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) {
                sb.append(line + "\n");
            }
            br.close();

            jsonString = sb.toString();

            System.out.println("JSON: " + jsonString);
        } catch (IOException e) {
            Log.e("DataRetriever", "exception", e);
        }

        return jsonString;
    }

    @Override
    protected void onPostExecute(String s) {
        if (s != null) {
            Log.d("DataRetriever", "Length: " + s.length());

            int airHum = 0;
            float airTemp = 0;
            int soilHum = 0;
            int light = 0;
            boolean pump = false;
            boolean lamp = false;

            try {
                JSONArray jArray = new JSONArray(s);
                JSONObject lastInfo = (JSONObject) jArray.get(0);

                airHum = Integer.parseInt(lastInfo.getString("air_humidity"));
                airTemp = Float.parseFloat(lastInfo.getString("air_temp"));
                soilHum = Integer.parseInt(lastInfo.getString("soil_humidity"));
                light = Integer.parseInt(lastInfo.getString("air_humidity"));
                pump = Boolean.parseBoolean(lastInfo.getString("ctrl_pump"));
                lamp = Boolean.parseBoolean(lastInfo.getString("ctrl_light"));


            } catch (JSONException e) {
                Log.e("DataRetriever", "exception", e);
            } catch (NumberFormatException e) {
                Log.e("DataRetriever", "exception", e);
            }
            dataListener.onDataReady(airHum, airTemp, soilHum, light, pump, lamp);
            return;
        }

            Log.d("DataRetriever", "null return");
        dataListener.onFail();
    }

    public interface DataListener {
        void onDataReady(int airHum, float airTemp, int soilHum, int light, boolean pump, boolean lamp);
        void onFail();
    }
}
