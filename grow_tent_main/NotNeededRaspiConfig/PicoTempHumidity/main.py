# main.py
# this is the primary code to use as of 7/2/2022

from machine import Pin
from time import sleep
import dht
 
 # remember to change sensor if using one other than an Inland DHT11
sensor = dht.DHT11(Pin(28)) 

# infinite loop to read and display data
# change to a fixed number in next branch 
while True:
    sensor.measure()
    temp = sensor.temperature()
    temp_f = temp * (9 / 5) + 32
    hum = sensor.humidity()
    print("Temperature: {}°C / {}°F  Humidity: {:.0f}% ".format(temp, temp_f, hum))
    sleep(.1)