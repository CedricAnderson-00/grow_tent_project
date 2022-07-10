# receiver.py / Tx/Rx => Tx/Rx
# connection between Raspberry Pi and Pico

import os
import machine
from time import sleep
from grow_tent_main.PicoFiles.TempHumiditySensor import get_temp_hum
from grow_tent_main.PicoFiles.light_sensor import readLight

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
    
    # flash led so user knows system is monitoring
    system_led = machine.Pin(25, machine.Pin.OUT)
    system_led.toggle()
    
    # placing the port here refreshes the port value each iteration
    uart = machine.UART(0, 115200)
    
    # nested loop to keep program running after displaying values
    # Onboard LED flashes to let user know system is monitoring
    while counter == 0:
        system_led.toggle()
        sleep(.1)
        if readLight(26) >= 50:
            pass
        else:
            pass
        y = ''
        # transfer values in tent state to master Pi
        # no call to functions here. will just read values from varaibles
        if uart.any() == 1:
            counter +=1
            while True:
                uart.write(str(x).encode('utf-8'))
                sleep(0.01)  # this depends on how much data is sent
                break
        
        # send data of second plant
        elif uart.any() == 2:
            print("second plant")
            break