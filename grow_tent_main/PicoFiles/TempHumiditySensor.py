# this is the primary code to use as of 7/2/2022

from machine import Pin
from time import sleep
import dht

# function to return values
def get_temp_hum():
    try:
        """function that is initiated from main.py to receive that average
        of the two temp/humidity sensors in tent
        """
        
        # remember to change sensor if using one other than an Inland DHT11
        sensor = dht.DHT11(Pin(10))
        sensor2 = dht.DHT11(Pin(11)) 

        # values of sensor 1  
        sensor.measure()
        temp = sensor.temperature()
        temp_f = temp * (9 / 5) + 32
        hum = sensor.humidity()

        # # values of sensor 2
        # sensor2.measure()
        # temp2 = sensor2.temperature()
        # temp_f2 = temp * (9 / 5) + 32
        # hum2 = sensor2.humidity()

        # # find tent average
        # avg_temp_f = (temp_f + temp_f2) / 2
        # avg_temp_c = (temp + temp2) / 2
        # avg_hum = (hum + hum2) / 2
    except (OSError, TypeError):  # catches this error if sensor if faulty. Prevents program from crashing
        return 0
    
    return temp, temp_f, hum


    # display averages
    # leave commented out. will use when button is pressed
    # temp_hum_report = print("Temperature: {}°C / {}°F  Humidity: {:.0f}% ".format(temp, temp_f, hum))