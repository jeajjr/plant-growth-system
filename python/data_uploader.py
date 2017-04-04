import sys
from phant import Phant


def postData(pubKey, privKey, air_humidity, air_temp, light, soil_humidity, ctrl_light, ctrl_pump):
    print("sending: ",air_humidity, air_temp, light, soil_humidity, ctrl_light, ctrl_pump)
    p = Phant(publicKey=pubKey,fields=["air_humidity","air_temp","light","soil_humidity","ctrl_light","ctrl_pump"],privateKey=privKey)

    try:
        p.log(air_humidity, air_temp, light, soil_humidity, ctrl_light, ctrl_pump)
        print('Data uploaded successfully')
    except:
        print('Failed to upload data')
