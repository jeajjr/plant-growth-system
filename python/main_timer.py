import config_ctrl
from datetime import time
from time import sleep
from sensor_reader import readAirHumidity, readAirTemperature, readSoilHumidity, readLightIntensity
from actuator_controller import setLight, setWaterPump
from data_uploader import postData

CONFIG_HAS_CHANGED = True

def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else:
        return nowTime >= startTime or nowTime <= endTime

def main():
    c = config_ctrl.Configurations()
    ctrl_light = False
    ctrl_pump = False

    setLight(ctrl_light)
    setWaterPump(ctrl_pump)

    while True:
        global CONFIG_HAS_CHANGED
        if CONFIG_HAS_CHANGED:
            CONFIG_HAS_CHANGED = False

            try:
                c = config_ctrl.readConfigurations()
            except:
                print('First time init. Saving standard configs.')
                config_ctrl.storeConfigurations(c)

        air_humidity = readAirHumidity()
        air_temp = readAirTemperature()
        light = readLightIntensity()
        soil_humidity = readSoilHumidity()

        if c.lightThresholdSelect == config_ctrl.LightThresholdEnum.LIGHT_SENSOR:
            if ctrl_light:
                if light > c.lightSensorUL:
                    ctrl_light = False
            else:
                if light < c.lightSensorLL:
                    ctrl_light = True
        else:
            if isNowInTimePeriod(c.lightTimeON, c.lightTimeOFF, datetime.now().time()):
                ctrl_light = True
            else:
                ctrl_light = False

        if c.waterPumpThresholdSelect == config_ctrl.WaterPumpThresholdEnum.MOISTURE:
            if ctrl_pump:
                if soil_humidity > c.waterPumpMoistureUL:
                    ctrl_pump = False
            else:
                if soil_humidity < c.waterPumpMoistureLL:
                    ctrl_pump = True
        else:
            print('Pump threshold: TIME')

        setLight(ctrl_light)
        setWaterPump(ctrl_pump)

        postData(pubKey="NJWqvnJNAyT0dNWZxrDd", privKey="5dPgkldVryuwJPZKaNBJ",
        air_humidity=air_humidity, air_temp=air_temp, light=light,
        soil_humidity=soil_humidity, ctrl_light=ctrl_light, ctrl_pump=ctrl_pump)

        sleep(c.sensorUpdatePeriod)

if __name__ == "__main__":
    main()
