# this is the primary code to use as of 7/2/2022

from machine import Pin
from time import sleep
import dht

# function to return values
def get_temp_hum():
    # remember to change sensor if using one other than an Inland DHT11
    sensor = dht.DHT11(Pin(28))
    sensor2 = dht.DHT11(Pin(27)) 

    # values of sensor 1  
    sensor.measure()
    temp = sensor.temperature()
    temp_f = temp * (9 / 5) + 32
    hum = sensor.humidity()

    # values of sensor 2
    sensor2.measure()
    temp2 = sensor2.temperature()
    temp_f2 = temp * (9 / 5) + 32
    hum2 = sensor2.humidity()

    # find tent average
    avg_temp_f = (temp_f + temp_f2) / 2
    avg_temp_c = (temp + temp2) / 2
    avg_hum = (hum + hum2) / 2
    
    return avg_temp_c, avg_temp_f, avg_hum


    # display averages
    # leave commented out. will use when button is pressed
    # temp_hum_report = print("Temperature: {}°C / {}°F  Humidity: {:.0f}% ".format(temp, temp_f, hum))