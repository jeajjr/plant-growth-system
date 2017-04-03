import sys
from phant import Phant


def postData(pubKey, privKey, air_humidity, air_temp, light, soil_humidity, ctrl_light, ctrl_pump):
    print("sending: ",air_humidity, air_temp, light, soil_humidity, ctrl_light, ctrl_pump)
#    p = Phant(publicKey=pubKey,fields=["air_humidity","air_temp","light","soil_humidity","ctrl_light","ctrl_pump"],privateKey=privKey)

#    p.log(air_humidity, air_temp, light, soil_humidity, ctrl_light, ctrl_pump)
#    print(p.remaining_bytes, p.cap)
