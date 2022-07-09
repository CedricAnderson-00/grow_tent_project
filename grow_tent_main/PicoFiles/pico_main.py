# receiver.py / Tx/Rx => Tx/Rx
# connection between Raspberry Pi and Pico

import os
import machine
from time import sleep
from grow_tent_main.PicoFiles.TempHumiditySensor import get_temp_hum

# to notify user that the program is running
# this will be moved into loop boody once program format is complete
print("*****Program running*****")

# loop that constantly runs to monitor state of UART
# counter will also dictate what plant to get data from
# main loop will monitor state of tent
# initiate a timer to grab data after a certain period
while True:
    # counter to limit inner loop iterations
    counter = 0
    
    # placing the port here refreshes the port value each iteration
    uart = machine.UART(0, 115200)
    
    # nested loop to keep program running after displaying values
    while counter == 0:
        print(".")
        sleep(1)
        y = ''
        # loop that will get values
        # transfer values in tent state to master Pi
        if uart.any() == 5:
            x = get_temp_hum()
            counter +=1
            y = [12345678901234]  # this simulates a list to pass to UART connection
            # while loop to send values and then wait for a response back to exit loop
            while True:
                uart.write(str(x).encode('utf-8'))
                sleep(0.01)  # this depends on how much data is sent
                break