from time import sleep
from machine import Timer, Pin, UART
from TempHumiditySensor import get_temp_hum
from SoilMoistureSensor import soil_sensor_one, soil_sensor_two, soil_sensor_three
from LcdDisplay import lcd
import _thread


# functions
def main_body(switch):
    """Function that sends and receives values from sensors. Takes one arguement that is used to monitor state of toggle switches"""
    
    global low_hum, low_temp_c, low_temp_f, light_time_on, light_time_off, pump_one_total, pump_two_total, pump_three_total, send_temp_c, send_hum, send_temp_f, fert_one_total, fert_two_total, fert_three_total
    
    while True:
    
        # flash led so user knows system is monitoring
        system_led = Pin(25, Pin.OUT)
        system_led.value(1)
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
                plant = 1, send_temp_f, send_temp_c, light_time_on, light_time_off, send_hum, soil1, pump_one_total, fert_one_total
                uart.write(str(plant).encode('utf-8'))
                sleep(0.01)  # this depends on how much data is sent
                pump_one_total = 0
                fert_one_total = 0
                
            elif uart.any() == 2:
                plant = 2, send_temp_f, send_temp_c, light_time_on, light_time_off, send_hum, soil2, pump_two_total, fert_two_total
                uart.write(str(plant).encode('utf-8'))
                sleep(0.01)  # this depends on how much data is sent
                pump_two_total = 0
                fert_two_total = 0

            elif uart.any() == 3:
                plant = 3, send_temp_f, send_temp_c, light_time_on, light_time_off, send_hum, soil3, pump_three_total, fert_three_total
                uart.write(str(plant).encode('utf-8'))
                sleep(0.01)  # this depends on how much data is sent
                pump_three_total = 0
                fert_three_total = 0
                
        return
                

def phase_switch_thread():
    """Function that creates a thread to monitor toggle switches to change grow parameters"""
    
    global phase_one, phase_two, phase_three, phase_four, toggle_one, toggle_two, toggle_three, toggle_four, grow_cycle
    
    if toggle_one.value() == 1:
        sleep(0.01)
        phase_one = True
        grow_cycle = 1
    elif toggle_two.value() == 1:
        sleep(0.01)
        phase_two = True
        grow_cycle = 2
    elif toggle_three.value() == 1:
        sleep(0.01)
        phase_three = True
        grow_cycle = 3
    elif toggle_four.value() == 1:
        sleep(0.01)
        phase_four = True
        grow_cycle = 4
    sleep(0.01)


def light_controller(t):
    """Function that monitors toggle switch state and initializes a light patter IAW switch parameters"""
    
    global light_time_on, tent_light_control, toggle_one, toggle_two, toggle_three, toggle_four, timer_one, light_time_off
    
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
    
    
def lights_on(t):
    """lights_on() turns tent light on and then waits a user-defined amount of time. 
       Adds time off to the global variable. After Timer is complete, calls lights_off()
       """
    
    global light_time_off, tent_light_control

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
    global pump_one, pump_two, pump_three, toggle_one, toggle_two, toggle_three, toggle_four
    
    # global dispensed values
    global pump_one_total, pump_two_total, pump_three_total
    
    # each pump is calibrated to always dispense a certain amount based off current phase per duty cycle
    large_mililiters = 250
    small_ml = 10
    
    # logic to dispense proper amounts based off switch status
    if toggle_one.value() == 1:
        pump_one.value(1)
        sleep(1)
        pump_one_total += small_ml
        pump_one.value(0)
        sleep(0.01)
        pump_two.value(1)
        sleep(1)
        pump_two_total += small_ml
        pump_two.value(0)
        sleep(0.01)
        pump_three.value(1)
        sleep(1)
        pump_three_total += small_ml
        pump_three.value(0)
        sleep(0.01)
    elif toggle_two.value() == 1:
        pump_one.value(1)
        sleep(1)
        pump_one_total += large_mililiters
        pump_one.value(0)
        sleep(0.01)
        pump_two.value(1)
        sleep(1)
        pump_two_total += large_mililiters
        pump_two.value(0)
        sleep(0.01)
        pump_three.value(1)
        sleep(1)
        pump_three_total += large_mililiters
        pump_three.value(0)
        sleep(0.01)
    elif toggle_three.value() == 1:
        pump_one.value(1)
        sleep(1)
        pump_one_total += large_mililiters
        pump_one.value(0)
        sleep(0.01)
        pump_two.value(1)
        sleep(1)
        pump_two_total += large_mililiters
        pump_two.value(0)
        sleep(0.01)
        pump_three.value(1)
        sleep(1)
        pump_three_total += large_mililiters
        pump_three.value(0)
        sleep(0.01)
    elif toggle_four.value() == 1:
        pump_one.value(0)
        sleep(0.01)
        pump_two.value(0)
        sleep(0.01)
        pump_three.value(0)
        sleep(0.01)
    elif toggle_five.value() == 1:
        pump_one.value(1)
        sleep(0)
        pump_one_total += small_ml
        pump_one.value(0)
        sleep(0.01)
        pump_two.value(1)
        sleep(0)
        pump_two_total += small_ml
        pump_two.value(0)
        sleep(0.01)
        pump_three.value(1)
        sleep(0)
        pump_three_total += small_ml
        pump_three.value(0)
        sleep(0.01)
    
    # recursion
    water_timer_switch = Timer(period=172_800_000, mode=Timer.ONE_SHOT, callback=fertilizer)  # timer to water two days 


def fertilizer(t):
    """Function that controls the dispensing of liquid fertilizers"""
    
    # global toggle switch state
    global toggle_one, toggle_two, toggle_three, toggle_four, toggle_five
    
    # global pump control
    global fert_one, fert_two, fert_three
    
    # global dispensed amounts
    global fert_one_total, fert_two_total, fert_three_total, stir_plate
    
    # each pump is calibrated to always dispense a certain amount based off current phase per duty cycle
    large_mililiters = 250
    small_ml = 10
    
    # same logic as water_plants()
    if toggle_one.value() == 1:
        stir_plate.value(1)
        sleep(1)
        stir_plate.value(0)
        sleep(0.01)
        fert_one.value(1)
        sleep(1)
        fert_one_total += small_ml
        fert_one.value(0)
        sleep(0.01)
        fert_two.value(1)
        sleep(1)
        fert_two_total += small_ml
        fert_two.value(0)
        sleep(0.01)
        fert_three.value(1)
        sleep(1)
        fert_three_total += small_ml
        fert_three.value(0)
        sleep(0.01)
    elif toggle_two.value() == 1 | toggle_three.value() == 1:  
        fert_one.value(1)
        sleep(1)
        fert_one_total += large_mililiters
        fert_one.value(0)
        sleep(0.01)
        fert_two.value(1)
        sleep(1)
        fert_two_total += large_mililiters
        fert_two.value(0)
        sleep(0.01)
        fert_three.value(1)
        sleep(1)
        fert_three_total += large_mililiters
        fert_three.value(0)
        sleep(0.01)
    elif toggle_four.value() == 1:
        fert_one.value(0)
        sleep(0.01)
        fert_two.value(0)
        sleep(0.01)
        pump_three.value(0)
        sleep(0.01)
    
    fert_timer = Timer(period=172_800_000, mode=Timer.ONE_SHOT, callback=water_plants)  # timer to fertilize every two days


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
fert_one_total = 0
fert_two_total = 0
fert_three_total = 0

# GPIO assignments
tent_light_control = Pin(12, Pin.OUT)
pump_one = Pin(15, Pin.OUT)
pump_two = Pin(14, Pin.OUT)
pump_three = Pin(13, Pin.OUT)
fert_one = Pin(20, Pin.OUT)
fert_two = Pin(21, Pin.OUT)
fert_three = Pin(22, Pin.OUT)
stir_plate = Pin(12, Pin.OUT)

# variables to start water and light cycles
timer_one = Timer(period=3_600_000, mode=Timer.PERIODIC, callback=light_controller)
_thread.start_new_thread(phase_switch_thread, ())

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
            water_plants(0)
            phase_switch_thread()
            main_body(toggle_one)
        while toggle_two.value() == 1:
            water_plants(0)
            phase_switch_thread()
            main_body(toggle_two)
        while toggle_three.value() == 1:
            water_plants(0)
            phase_switch_thread()
            main_body(toggle_three)
        while toggle_four.value() == 1:
            water_plants(0)
            phase_switch_thread()
            main_body(toggle_four)
        