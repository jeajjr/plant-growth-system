package tk.jealmas.plantgrowthcontroller;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import tk.jealmas.plantgrowthcontroller.data.ConfigTransmitter;
import tk.jealmas.plantgrowthcontroller.data.DataRetriever;

public class ActivityMain extends Activity {

    private Button commandButton;
    private Button dataButton;

    private TextView textAirHum;
    private TextView textAirTemp;
    private TextView textSoilHum;
    private TextView textLightSensor;
    private TextView textPump;
    private TextView textLight;

    private TextView commandText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        commandButton = (Button) findViewById(R.id.buttonCommand);
        dataButton = (Button) findViewById(R.id.buttonData);

        textAirHum = (TextView) findViewById(R.id.textAirHum);
        textAirTemp = (TextView) findViewById(R.id.textAirTemp);
        textSoilHum = (TextView) findViewById(R.id.textSoilHum);
        textLight = (TextView) findViewById(R.id.textLight);
        textPump = (TextView) findViewById(R.id.textPump);
        textLightSensor = (TextView) findViewById(R.id.textLightSensor);

        commandText = (TextView) findViewById(R.id.textCommand);

        commandButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                (new ConfigTransmitter(new ConfigTransmitter.ConfigTransmitterListener() {
                    @Override
                    public void onSuccess() {
                        commandText.setText("OK");
                    }

                    @Override
                    public void onFail() {
                        commandText.setText("FALHA");
                    }
                })).execute();
            }
        });

        dataButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                (new DataRetriever(new DataRetriever.DataListener() {
                    @Override
                    public void onDataReady(int airHum, float airTemp, int soilHum, int light, boolean pump, boolean lamp) {
                        textAirHum.setText("Umidade do ar: " + airHum + " %");
                        textAirTemp.setText("Temperatura do ar: " + String.format("%.1f C", airTemp));
                        textSoilHum.setText("Umidade do solo: " + soilHum + " %");
                        textLightSensor.setText("Intensidade de luz: " + light + " %");

                        if (pump)
                            textPump.setText("Bomba d'água: ON");
                        else
                            textPump.setText("Bomba d'água: OFF");

                        if (lamp)
                            textLight.setText("Lampada: ON");
                        else
                            textLight.setText("Lampada: OFF");

                    }

                    @Override
                    public void onFail() {
                        Toast.makeText(ActivityMain.this, "Falha na obtenção dos dados", Toast.LENGTH_LONG);
                    }
                })).execute();
            }
        });
    }
}
