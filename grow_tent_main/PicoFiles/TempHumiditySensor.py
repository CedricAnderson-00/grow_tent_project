# this is the primary code to use as of 7/2/2022

from machine import Pin, I2C
from time import sleep
import dht

# function to return values
def get_temp_hum(sensor):
    
    try:
        """function that is initiated from main.py to receive that average
        of the two temp/humidity sensors in tent
        """
        if sensor == "dht11":
            
            # remember to change sensor if using one other than an Inland DHT11
            sensor = dht.DHT11(Pin(7))

            # values of sensor 1  
            sensor.measure()
            temp_c = sensor.temperature()
            temp_f = temp * (9 / 5) + 32
            humidity = sensor.humidity()
            
        elif sensor == "sht31":
            
            # Start i2c bus
            i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
            
            # send start conversion command
            i2c.writeto(0x44, bytes([0x2C, 0x06]))

            # wait for the conversion to complete
            sleep(0.5)

            # Read the data from the SHT31 containing
            # the temperature (16-bits + CRC) and humidity (16bits + crc)
            data = i2c.readfrom_mem(0x44, 0x00, 6)

            # Convert the data
            temp = data[0] * 256 + data[1]
            temp_c = -45 + (175 * temp / 65535.0)
            temp_f = temp_c * (9/5) + 32
            humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
            
    except (OSError, TypeError):  # catches this error if sensor if faulty. Prevents program from crashing
        return 0
    
    return temp_c, temp_f, humidity
