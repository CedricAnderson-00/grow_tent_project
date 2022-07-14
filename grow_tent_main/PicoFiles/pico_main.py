# receiver.py / Tx/Rx => Tx/Rx
# connection between Raspberry Pi and Pico

import os
import machine
from time import sleep
from machine import Timer
from grow_tent_main.PicoFiles.TempHumiditySensor import get_temp_hum
from grow_tent_main.PicoFiles.light_sensor import readLight
import grow_tent_main.PicoFiles.plants as Plant

# start timer for lights
def mycallback(t):
    print("complete")
    
test_timer = Timer(period=10000, mode=Timer.PERIODIC, callback=mycallback)

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
    system_led.value(1)
    
    # placing the port here refreshes the port value each iteration
    uart = machine.UART(0, 115200)
    
    # nested loop to keep program running after displaying values
    while counter == 0:  # change to number of plants
        system_led.toggle()
        x = get_temp_hum()
        send_temp_c = x[1]
        send_temp_f = x[2]
        send_hum = x[3]
        if readLight(26) >= 50:
            pass
        else:
            pass
        # transfer values in tent state to master Pi
        # no call to functions here. will just read values from varaibles
        if uart.any() == 1:
            counter +=1
            plant1 = Plant()
            while True:
                uart.write(str(x).encode('utf-8'))
                sleep(0.01)  # this depends on how much data is sent
                break
        elif uart.any() == 2:
            print("second plant")
            break