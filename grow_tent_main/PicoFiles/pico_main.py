# receiver.py / Tx/Rx => Tx/Rx
# connection between Raspberry Pi and Pico

import os
import machine
from time import sleep
from main import from_pi

# port to establish connection
uart = machine.UART(0, 115200)

# to notify user that the program is running
# this will be moved into loop boody once program format is complete
print("*****Program running*****")

while True:
    print(".")
    sleep(1)
    if uart.any():
        x = from_pi()  # this function will house all of the sensor data
        uart.write(str(x))  # only know how to send strings through UART connection