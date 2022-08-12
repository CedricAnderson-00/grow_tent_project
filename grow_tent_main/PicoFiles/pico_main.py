from time import sleep
from machine import Timer, Pin
from grow_tent_main.PicoFiles.TempHumiditySensor import get_temp_hum
from grow_tent_main.PicoFiles.SoilMoistureSensor import soil_sensor_one, soil_sensor_two, soil_sensor_three
from views.LcdDisplay import lcd
import _thread


# functions
def phase_switch_thread():
    """Function that creates a thread to monitor toggle switches to change grow parameters"""
    
    global phase_one, phase_two, phase_three, phase_four, toggle_one, toggle_two, toggle_three, toggle_four
    
    if toggle_one.value() == 1:
        phase_one = True
    elif toggle_two.value() == 1:
        phase_two = True
    elif toggle_three.value() == 1:
        phase_three = True
    elif toggle_four.value() == 1:
        phase_four = True
    sleep(0.01)
_thread.start_new_thread(phase_switch_thread, ())


def continous_lights():
    """Function for plants that require constant light. Increments every hour."""
    
    global light_time_on, tent_light_control
    
    tent_light_control.value(1)
    hour_timer = Timer(period=3_600_000, mode=Timer.PERIODIC, callback=continous_lights)  # 1 hour in milliseconds
    light_time_on +=1  # increase overall timer by 1 hour
    
    
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
    
    
def waterPlants(t):
    """Function to water each plant for a set amount of time depending on calibration.
       Uses recurrsion to start a timer to repeat in 48 hours
       """
    # global GPIO control   
    global pump_one, pump_two, pump_three, toggle_one, toggle_two, toggle_three, toggle_four
    
    # global dispensed values
    global pump_one_total, pump_two_total, pump_three_total
    
    # each pump is calibrated to always dispense a certain amount based off current phase per duty cycle
    veg_mililiters = 250
    seedling_ml = 10
    
    # logic to dispense proper amounts based off switch status
    if toggle_one.value() == 1:
        pump_one.value(1)
        sleep(10)
        pump_one_total += seedling_ml
        pump_one.value(0)
        pump_two.value(1)
        sleep(10)
        pump_two_total += seedling_ml
        pump_two.value(0)
        pump_three.value(1)
        sleep(10)
        pump_three_total += seedling_ml
        pump_three.value(0)
    elif toggle_two.value() == 1 | toggle_three.value() == 1:  
        pump_one.value(1)
        sleep(100)
        pump_one_total += veg_mililiters
        pump_one.value(0)
        pump_two.value(1)
        sleep(100)
        pump_two_total += veg_mililiters
        pump_two.value(0)
        pump_three.value(1)
        sleep(100)
        pump_three_total += veg_mililiters
        pump_three.value(0)
    elif toggle_four.value() == 1:
        Timer.deinit(water_timer)
        pump_one.value(0)
        pump_two.value(0)
        pump_three.value(0)
    
    # recursion
    water_timer = Timer(period=172_800_000, mode=Timer.ONE_SHOT, callback=fertilizer)  # timer to water every other day


def fertilizer(t):
    """Function that controls the dispensing of liquid fertilizers"""
    
    # global pump control
    global fert_one, fert_two, fert_three
    
    # global dispensed amounts
    global fert_one_total, fert_two_total, fert_three_total
    
    # each pump is calibrated to always dispense a certain amount based off current phase per duty cycle
    veg_mililiters = 250
    seedling_ml = 10
    
    # same logic as waterPlants()
    if toggle_one.value() == 1:
        fert_one.value(1)
        sleep(10)
        fert_one_total += seedling_ml
        fert_one.value(0)
        fert_two.value(1)
        sleep(10)
        fert_two_total += seedling_ml
        fert_two.value(0)
        fert_three.value(1)
        sleep(10)
        fert_three_total += seedling_ml
        fert_three.value(0)
    elif toggle_two.value() == 1 | toggle_three.value() == 1:  
        fert_one.value(1)
        sleep(100)
        fert_one_total += veg_mililiters
        fert_one.value(0)
        fert_two.value(1)
        sleep(100)
        fert_two_total += veg_mililiters
        fert_two.value(0)
        fert_three.value(1)
        sleep(100)
        fert_three_total += veg_mililiters
        fert_three.value(0)
    elif toggle_four.value() == 1:
        Timer.deinit(fert_timer)
        fert_one.value(0)
        fert_two.value(0)
        pump_three.value(0)
    
    fert_timer = Timer(period=172_800_000, mode=Timer.ONE_SHOT, callback=waterPlants)  # timer to water every other day
    
def display_lcd():
    """Timed function that transmits data to LCDs"""
    
    # hex addresses for lcd(s)
    # SDA(8) SCL(9)
    lcd_one = 0x27  # temperature f
    lcd_two = 0x26  # temperature c
    lcd_three = 0x25  # humidity
    lcd_four = 0x23  # lights
    
    global send_hum, send_temp_c, send_temp_f, low_hum, low_temp_f, low_temp_c, light_time_on, light_time_off
    
    lcd(lcd_one, str(send_temp_f), str(low_temp_f), 1)
    lcd(lcd_two, str(send_temp_c), str(low_temp_c), 2)
    lcd(lcd_three, str(send_hum), str(low_hum), 3) 
    lcd(lcd_four, str(light_time_on), str(light_time_off), 4) 
        
    return
    

# toggle switch GPIO
toggle_one = Pin(16, Pin.IN, Pin.PULL_DOWN)
toggle_two = Pin(17, Pin.IN, Pin.PULL_DOWN)
toggle_three = Pin(18, Pin.IN, Pin.PULL_DOWN)
toggle_four = Pin(19, Pin.IN, Pin.PULL_DOWN)


# global variables for switches
phase_one = False
phase_two = False
phase_three = False
phase_four = False
    
# timer values 
light_time_on = 0000
light_time_off = 0000
pump_one_total = 0000
pump_two_total = 0000
pump_three_total = 0000
fert_one_total = 0000
fert_two_total = 0000
fert_three_total = 0000

# GPIO assignments
tent_light_control = Pin(12, Pin.OUT)
pump_one = Pin(15, Pin.IN)
pump_two = Pin(14, Pin.IN)
pump_three = Pin(13, Pin.IN)
fert_one = Pin(20, Pin.IN)
fert_two = Pin(21, Pin.IN)
fert_three = Pin(22, Pin.IN)

# variables to start water and light cycles  
# program_start_timer = Timer(period=3_600_000, mode=Timer.ONE_SHOT, callback=lightsOff)
waterPlants()
continous_lights()
display_timer = Timer(period=60_000, mode=Timer.PERIODIC, callback=display_lcd)  # updates lcd(s) every minute

# low values
# set to maximum values for initial running of program to establish low values
low_temp_f = 212
low_temp_c = 100
low_hum = 100

# to notify user that the program is running
# delete after R/D
print("*****Program running*****")

# loop that constantly runs to monitor state of UART
# counter will also dictate what plant to get data from
# main loop will monitor state of tent
# initiate a timer to grab data after a certain period
while True:

    # flash led so user knows system is monitoring
    system_led = machine.Pin(25, machine.Pin.OUT)
    system_led.value(1)
    
    # nested loop to keep program running after displaying values
    while True:  # change to number of plants
        uart = machine.UART(0, 115200)
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
            plant = counter, send_temp_f, send_temp_c, light_time_on, light_time_off, send_hum, soil1, pump_one_total
            uart.write(str(plant).encode('utf-8'))
            sleep(0.01)  # this depends on how much data is sent
            pump_one_total = 0
              
        elif uart.any() == 2:
            plant = counter, send_temp_f, send_temp_c, light_time_on, light_time_off, send_hum, soil2, pump_two_total
            uart.write(str(plant).encode('utf-8'))
            sleep(0.01)  # this depends on how much data is sent
            pump_two_total = 0

        elif uart.any() == 3:
            plant = 3, send_temp_f, send_temp_c, light_time_on, light_time_off, send_hum, soil3, pump_three_total
            uart.write(str(plant).encode('utf-8'))
            sleep(0.01)  # this depends on how much data is sent
            pump_three_total = 0

