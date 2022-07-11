# change to main.py when ready to upload to Pico
# monitors and controls the activation of heating elements.

from machine import Pin
from time import sleep
import dht

# assign GPIO pin locations
emergency_cooling = Pin(18, Pin.OUT)
dehumidifier = Pin(19, Pin.OUT)
heat_control = Pin(16, Pin.OUT)
hum_control = Pin(17, Pin.OUT)
sensor = dht.DHT11(Pin(28))
led_onboard = Pin(25, Pin.OUT)

# while loop to continuosly monitor system
while True:
    try:
        led_onboard.toggle()
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        temp_f = temp * (9 / 5) + 32
        
        # logic to test current state of system
        if temp_f > 70 < 85:
            heat_control.value(0)
            emergency_cooling.value(0)
        elif temp_f > 85:
            emergency_cooling.value(1)    
        else:
            heat_control.value(1)
            
        # this logic will check humidity levels and operate relay
        if hum > 40 < 50:
            hum_control.value(0)
            dehumidifier.value(0)
        elif hum >= 50:
            dehumidifier.value(1)
        else:
            hum_control.value(1)
        
    except OSError:
        print("no reading from sensor")
        heat_control.value(0)
