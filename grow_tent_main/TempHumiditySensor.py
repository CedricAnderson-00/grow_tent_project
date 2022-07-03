# main.py
# this is the primary code to use as of 7/2/2022

from machine import Pin
from time import sleep
import dht
 
 # remember to change sensor if using one other than an Inland DHT11
sensor = dht.DHT11(Pin(28)) 

# values to be imported from main.py  
sensor.measure()
temp = sensor.temperature()
temp_f = temp * (9 / 5) + 32
hum = sensor.humidity()
temp_hum_report = print("Temperature: {}°C / {}°F  Humidity: {:.0f}% ".format(temp, temp_f, hum))