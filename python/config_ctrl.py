from enum import Enum
import datetime
import pickle

configurationFile = '.config'

# Defines the possible thresholds for turning on the light
class LightThresholdEnum(Enum):
    LIGHT_SENSOR = 1    # turn on and off according to thresholds
    TIME = 2            # turn on and off at specific hours every day

# Defines the possible thresholds for turning on the water pump
class WaterPumpThresholdEnum(Enum):
    MOISTURE = 1    # turn on and off according to moisture thresholds
    TIME = 2        # turn on and off in a specific period with a specific duration

class Configurations(object):
    def __init__(self):
        # Light thresholds
        self.lightThresholdSelect = LightThresholdEnum.TIME
        self.lightSensorUL = 45
        self.lightSensorLL = 40
        self.lightTimeON = datetime.time(22, 00)
        self.lightTimeOFF = datetime.time(2, 00)

        # Water Pump thresholds
        self.waterPumpThresholdSelect = WaterPumpThresholdEnum.MOISTURE
        self.waterPumpMoistureUL = 80
        self.waterPumpMoistureLL = 40
        self.waterPumpTimePeriod = datetime.time(1, 00)
        self.waterPumpTimeDuration = datetime.time(0, 10)

        self.publicKey = ""
        self.privateKey = ""

        self.sensorUpdatePeriod = 2 # seconds

def storeConfigurations(config):
    with open(configurationFile, 'wb') as output:
        pickle.dump(config, output, pickle.HIGHEST_PROTOCOL)

def readConfigurations():
    with open(configurationFile, 'rb') as input:
        configs = pickle.load(input)
        return configs
