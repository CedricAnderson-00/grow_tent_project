# module to detect how long lights have been on
# using resistor with double brown lines 10k ohms possibly

from machine import ADC, Pin
from time import sleep

def readLight(pin1, pin2):
    """readLight takes two arguements that represent set pin values
       Compares the two values to determine if a sensor is bad.
       If large difference, a null value is returned
       """
      
    photoRes = ADC(Pin(pin1))
    photoRes2 = ADC(Pin(pin2))  # write logic to compare values
    light = photoRes.read_u16()  # reading 16bits
    
    # find ideal lighting values and adjust to required needs
    light = round(light/65535*100,2) 
    return light


# this is for testing purposes.
# will import readLight() function seperately
# while True:
#     print("Light: " + str(readLight(photoPIN)) +"%")
#     sleep(1)