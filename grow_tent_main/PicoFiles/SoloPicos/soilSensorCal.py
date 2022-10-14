from machine import ADC, Pin
import utime

# assign GPIO pin
soil = ADC(Pin(26))

# Variables
min_moisture = 0
max_moisture = 65535    
readDelay = 0.5

# loop to get reading
while True:
    moisture = (max_moisture-soil.read_u16()) * 100 / (max_moisture - min_moisture)
    utime.sleep(readDelay)