import config_ctrl
from datetime import time
from time import sleep
from sensor_reader import readAirHumidity, readAirTemperature, readSoilHumidity, readLightIntensity
from actuator_controller import setLight, setWaterPump
from data_uploader import postData
import threading
import socket
import struct

CONFIG_HAS_CHANGED = True


class ConfigServerSpawner(threading.Thread):
    def __init__(self,port):
        self.__port = port
        threading.Thread.__init__(self)

    def run(self):
        self.host = '0.0.0.0'
        self.port = self.__port
        print('starting  connection on', self.host, self.port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        while True:
            client, address = self.sock.accept()
            ConfigServer(client, address).start()

class ConfigServer(threading.Thread):
    def __init__(self,client, address):
        self.__client = client
        self.__address = address
        threading.Thread.__init__(self)

    def run(self):
        client = self.__client
        address = self.__address
        print('got connection from ', address)
        try:
            _command = client.recv(4)
            command = struct.unpack('!i', _command)[0]
            _length = client.recv(4)
            length = struct.unpack('!i', _length)[0]
            data = client.recv(length)

            print('received command', command, 'data', data)
            # TODO: parse command and apply configurationFile

            client.send(b'\x00')
        except Exception as e:
            print(str(e))
            client.send(b'\x01')
            client.close()
            return False

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

    ConfigServerSpawner(5001).start()

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
