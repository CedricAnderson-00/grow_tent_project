import os
import machine
from time import sleep
from machine import Timer, Pin
from grow_tent_main.PicoFiles.TempHumiditySensor import get_temp_hum
from grow_tent_main.PicoFiles.light_sensor import readLight
import grow_tent_main.PicoFiles.plants as Plant


# functions
def lightsOn(t):
    """lights_on() turns tent light on and then waits a user-defined amount of time. 
       Adds time off to the global variable. After Timer is complete, calls lights_off()
       """
    
    global light_time_off, tent_light_control
    
    tent_light_control.value(1)
    light_time_off += 1
    timer_off = Timer(period=500, mode=Timer.ONE_SHOT, callback=lightsOff)
    

def lightsOff(t):
    """lights_off() turns tent light off and then waits a user-defined amount of time. 
       Adds time on to the global variable. After Timer is complete, calls lights_on()
       """
       
    global light_time_on, tent_light_control
    
    tent_light_control.value(0)
    light_time_on += 1
    timer_on = Timer(period=500, mode=Timer.ONE_SHOT, callback=lightsOn)
    
    
def waterPlants():
    """Function to water each plant for a set amount of time depending on calibration.
       Uses recurrsion to start a timer to repeat in 48 hours
       """
    # global GPIO control   
    global pump_one, pump_two, pump_three
    
    # global dispensed values
    global pump_one_total, pump_two_total, pump_three_total
    
    # each pump is calibrated to always dispense 250ml per duty cycle
    mililiters = 250
    
    pump_one.value(1)
    sleep(5)
    pump_one_total += mililiters
    pump_one.value(0)
    pump_two.value(1)
    sleep(6)
    pump_two_total += mililiters
    pump_two.value(0)
    pump_three.value(1)
    sleep(7)
    pump_three_total += mililiters
    pump_three.value(0)
    
    # recursion
    water_timer = Timer(period=172_800_000, mode=Timer.ONE_SHOT, callback=waterPlants)
    

# variables to start water and light cycles  
program_start_timer = Timer(period=10000, mode=Timer.ONE_SHOT, callback=lightsOff)
waterPlants()

# timer values to input into MySQL
light_time_on = 0000
light_time_off = 0000
pump_one_total = 0000
pump_two_total = 0000
pump_three_total = 0000

# GPIO assignments
tent_light_control = Pin(17, Pin.OUT)
pump_one = Pin(15, Pin.IN)
pump_two = Pin(14, Pin.IN)
pump_three = Pin(13, Pin.IN)

# to notify user that the program is running
# delete after R/D
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
        send_temp_c = x[0]
        send_temp_f = x[1]
        send_hum = x[2]

        # transfer values in tent state to master Pi
        # no call to functions here. will just read values from varaibles
        # add soil logic here
        if uart.any() == 1:
            counter +=1
            plant = Plant(counter, send_temp_f, send_temp_c, light_time_on, light_time_off, send_hum, pump_one_total)
            while True:
                uart.write(str(plant).encode('utf-8'))
                sleep(0.01)  # this depends on how much data is sent
                pump_one_total = 0
                break
        elif uart.any() == 2:
            plant = Plant(counter, send_temp_f, send_temp_c, light_time_on, light_time_off, send_hum, pump_two_total)
            while True:
                uart.write(str(plant).encode('utf-8'))
                sleep(0.01)  # this depends on how much data is sent
                pump_two_total = 0
                break
        elif uart.any() == 3:
            plant = Plant(counter, send_temp_f, send_temp_c, light_time_on, light_time_off, send_hum, pump_three_total)
            while True:
                uart.write(str(plant).encode('utf-8'))
                sleep(0.01)  # this depends on how much data is sent
                pump_three_total = 0
                break