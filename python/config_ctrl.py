from enum import Enum
import datetime
import pickle

configurationFile = '.config'

# Defines the possible thresholds for turning on the light
class LightThresholdEnum(Enum):
    LIGHT_SENSOR = 1
    TIME = 2

# Defines the possible thresholds for turning on the water pump
class WaterPumpThresholdEnum(Enum):
    MOISTURE = 1
    TIME = 2

class Configurations(object):
    def __init__(self):
        # Light thresholds
        self.lightThresholdSelect = LightThresholdEnum.LIGHT_SENSOR
        self.lightSensorUL = 40
        self.lightSensorLL = 45
        self.lightTimeON = datetime.time(22, 00)
        self.lightTimeOFF = datetime.time(2, 00)

        # Water Pump thresholds
        self.waterPumpThresholdSelect = WaterPumpThresholdEnum.MOISTURE
        self.waterPumpMoistureUL = 80
        self.waterPumpMoistureLL = 40
        self.waterPumpTimePeriod = datetime.time(1, 00)
        self.waterPumpTimeDuration = datetime.time(0, 10)

def StoreConfigurations(config: Configurations):
    with open(configurationFile, 'wb') as output:
        pickle.dump(config, output, pickle.HIGHEST_PROTOCOL)

def ReadConfigurations():
    with open(configurationFile, 'rb') as input:
        configs = pickle.load(input)
        return configs
