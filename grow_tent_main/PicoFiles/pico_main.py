from time import sleep
from machine import Timer, Pin, UART
from TempHumiditySensor import get_temp_hum
from SoilMoistureSensor import soil_sensor_one, soil_sensor_two, soil_sensor_three
import _thread


# functions
def main_body(switch):
    """Function that sends and receives values from sensors. Takes one arguement that is used to monitor state of toggle switches"""
    
    global low_hum, low_temp_c, low_temp_f, light_time_on, light_time_off, pump_one_total, pump_two_total, pump_three_total, send_temp_c, send_hum, send_temp_f, 
    
    while True:
    
        # flash led so user knows system is monitoring
        system_led = Pin(25, Pin.OUT)
        system_led.value(1)
        light_controller(1)
        while switch.value() == 1:
            if toggle_five.value() == 1:
                water_plants(0)  
            uart = UART(0, 115200)
            system_led.toggle()
            x = get_temp_hum()
            send_temp_c = x[0]
            send_temp_f = x[1]
            send_hum = x[2]
            
            # logic to get low and high values
            if send_hum < low_hum:
                low_hum = send_hum
                
            if send_temp_c < low_temp_c:
                low_temp_c = send_temp_c
                
            if send_temp_f < low_temp_f:
                low_temp_f = send_temp_f
                
            # get soil readings    
            soil1 = soil_sensor_one()
            soil2 = soil_sensor_two()
            soil3 = soil_sensor_three()

            # transfer values in tent state to master Pi
            if uart.any() == 1:
                plant = 1, send_temp_f, send_temp_c, light_time_on, light_time_off, send_hum, soil1, pump_one_total
                uart.write(str(plant).encode('utf-8'))
                sleep(0.01)  # this depends on how much data is sent
                pump_one_total = 0
                
            elif uart.any() == 2:
                plant = 2, send_temp_f, send_temp_c, light_time_on, light_time_off, send_hum, soil2, pump_two_total
                uart.write(str(plant).encode('utf-8'))
                sleep(0.01)  # this depends on how much data is sent
                pump_two_total = 0

            elif uart.any() == 3:
                plant = 3, send_temp_f, send_temp_c, light_time_on, light_time_off, send_hum, soil3, pump_three_total
                uart.write(str(plant).encode('utf-8'))
                sleep(0.01)  # this depends on how much data is sent
                pump_three_total = 0
                
            sleep(0.1)
                
        return


def light_controller(t):
    """Function that monitors toggle switch state and initializes a light patter IAW switch parameters"""
    
    global light_time_on, tent_light_control, toggle_one, toggle_two, toggle_three, toggle_four, timer_one, light_time_off
    
    try:
        if toggle_one.value() == 1 | toggle_two.value() == 1:
            tent_light_control.value(1)
            sleep(0.01)
            light_time_on +=1
        if toggle_three.value() == 1:
            Timer.deinit(timer_one)
            lights_off(0)
        elif toggle_four.value() == 1:
            Timer.deinit(timer_one)
            lights_off(0)
    except: NameError
    
def lights_on(t):
    """lights_on() turns tent light on and then waits a user-defined amount of time. 
       Adds time off to the global variable. After Timer is complete, calls lights_off()
       """
    
    global light_time_off, tent_light_control

    # add a condition check here
    tent_light_control.value(1)
    sleep(0.01)
    light_time_off += 12
    large_timer_off = Timer(period=43_200_000, mode=Timer.ONE_SHOT, callback=lights_off)  # 12 hours in ms
    

def lights_off(t):
    """lights_off() turns tent light off and then waits a user-defined amount of time. 
       Adds time on to the global variable. After Timer is complete, calls lights_on()
       """
       
    global light_time_on, tent_light_control
    
    tent_light_control.value(0)
    sleep(0.01)
    light_time_on += 12
    large_timer_off = Timer(period=43_200_000, mode=Timer.ONE_SHOT, callback=lights_on)  # 12 hours in ms
    
    
def water_plants(t):
    """Function to water each plant for a set amount of time depending on calibration.
       Uses recurrsion to start a timer to repeat in 48 hours
       """
        
    # global GPIO control   
    global pump_one, toggle_one, toggle_two, toggle_three, toggle_four
    
    # global dispensed values
    global pump_one_total, pump_two_total, pump_three_total
    
    # each pump is calibrated to always dispense a certain amount based off current phase per duty cycle
    large_mililiters = 550
    small_ml = 100
    
    # logic to dispense proper amounts based off switch status
    if toggle_one.value() == 1:
        pump_one.value(1)
        sleep(10)
        pump_one_total += small_ml
        pump_two_total += small_ml
        pump_three_total += small_ml
        pump_one.value(0)
    elif toggle_two.value() == 1:
        pump_one.value(1)
        sleep(55)
        pump_one_total += large_mililiters
        pump_two_total += large_mililiters
        pump_three_total += large_mililiters
        pump_one.value(0)
    elif toggle_three.value() == 1:
        pump_one.value(1)
        sleep(55)
        pump_one_total += large_mililiters
        pump_two_total += large_mililiters
        pump_three_total += large_mililiters
        pump_one.value(0)
    elif toggle_four.value() == 1:
        pump_one.value(1)
        sleep(55)
        pump_one_total += large_mililiters
        pump_two_total += large_mililiters
        pump_three_total += large_mililiters
        pump_one.value(0)
    elif toggle_five.value() == 1:
        pump_one.value(1)
        sleep(10)
        pump_one_total += 110
        pump_two_total += 110
        pump_three_total += 110
        pump_one.value(0)
    
    # recursion
    water_timer_switch = Timer(period=43_200_000, mode=Timer.PERIODIC, callback=water_plants)  # timer to water every 12 hrs 43200000


# toggle switch GPIO
toggle_one = Pin(16, Pin.IN, Pin.PULL_DOWN)
toggle_two = Pin(17, Pin.IN, Pin.PULL_DOWN)
toggle_three = Pin(18, Pin.IN, Pin.PULL_DOWN)
toggle_four = Pin(19, Pin.IN, Pin.PULL_DOWN)
toggle_five = Pin(6, Pin.IN, Pin.PULL_DOWN)

# timer values 
light_time_on = 0
light_time_off = 0
pump_one_total = 0
pump_two_total = 0
pump_three_total = 0

# GPIO assignments
tent_light_control = Pin(12, Pin.OUT)
pump_one = Pin(15, Pin.OUT)  # water

# turn off relays to prevent short in circuit
pump_one.value(0)
tent_light_control.value(0)
sleep(1)

# variables to start water and light cycles
tent_light_control.value(1)
water_plants(1)
timer_one = Timer(period=3_600_000, mode=Timer.PERIODIC, callback=light_controller)


# low values
# set to maximum values for initial running of program to establish low values
low_temp_f = 212
low_temp_c = 100
low_hum = 100
grow_cycle = 0

# notify user that the program is running
print("*****Program running*****")

# loop that constantly runs to monitor state of UART
while True:

    # solid LED to let user know system is in standby
    system_led = Pin(25, Pin.OUT)
    system_led.value(1)
    while True:  # change to number of plants
        while toggle_one.value() == 1:
            main_body(toggle_one)
        while toggle_two.value() == 1:
            main_body(toggle_two)
        while toggle_three.value() == 1:
            light_controller(1)
            main_body(toggle_three)
        while toggle_four.value() == 1:
            light_controller(1)
            main_body(toggle_four)
        
