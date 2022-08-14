from time import sleep
from machine import Timer, Pin, UART
from TempHumiditySensor import get_temp_hum
from SoilMoistureSensor import soil_sensor_one, soil_sensor_two, soil_sensor_three
from LcdDisplay import lcd
import _thread


# functions
def main_body(switch):
    
    global low_hum, low_temp_c, low_temp_f, light_time_on, light_time_off, pump_one_total, pump_two_total, pump_three_total, send_temp_c, send_hum, send_temp_f, system_monitoring
    
    while True:
    
        # flash led so user knows system is monitoring
        system_led = Pin(25, Pin.OUT)
        system_led.value(1)
        system_monitoring = True
        water_plants(0)
        light_controller(0)
        display_lcd(0)
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
                
        return
                


def phase_switch_thread():
    """Function that creates a thread to monitor toggle switches to change grow parameters"""
    
    global phase_one, phase_two, phase_three, phase_four, toggle_one, toggle_two, toggle_three, toggle_four, grow_cycle
    
    if toggle_one.value() == 1:
        print('phase 1')
        phase_one = True
        grow_cycle = 1
    elif toggle_two.value() == 1:
        phase_two = True
        grow_cycle = 2
    elif toggle_three.value() == 1:
        phase_three = True
        grow_cycle = 3
    elif toggle_four.value() == 1:
        phase_four = True
        grow_cycle = 4
    sleep(0.01)


def light_controller(t):
    """Function that monitors toggle switch state and initializes a light patter IAW switch parameters"""
    
    global light_time_on, tent_light_control, toggle_one, toggle_two, toggle_three, toggle_four
    
    if toggle_one.value() == 1 | toggle_two.value() == 1:
        tent_light_control.value(1)
        hour_timer = Timer(period=3_600_000, mode=Timer.ONE_SHOT, callback=light_controller)  # 1 hour in milliseconds
        light_time_on +=1  
    elif toggle_three.value() == 1:
        tent_light_control.value(0)
        veg_timer_on = Timer(period=43_200_000, mode=Timer.ONE_SHOT, callback=lights_on)  # 12 hours in ms
    elif toggle_four.value() == 1:
        tent_light_control.value(0)
    
    
def lights_on(t):
    """lights_on() turns tent light on and then waits a user-defined amount of time. 
       Adds time off to the global variable. After Timer is complete, calls lights_off()
       """
    
    global light_time_off, tent_light_control
    
    tent_light_control.value(1)
    light_time_off += 12
    veg_timer_off = Timer(period=43_200_000, mode=Timer.ONE_SHOT, callback=lights_off)  # 12 hours in ms
    

def lights_off(t):
    """lights_off() turns tent light off and then waits a user-defined amount of time. 
       Adds time on to the global variable. After Timer is complete, calls lights_on()
       """
       
    global light_time_on, tent_light_control
    
    tent_light_control.value(0)
    light_time_on += 12
    light_controller()
    
    
def water_plants(t):
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
        print('pumps on')
        pump_one.value(1)
        sleep(0)
        pump_one_total += seedling_ml
        pump_one.value(0)
        pump_two.value(1)
        sleep(0)
        pump_two_total += seedling_ml
        pump_two.value(0)
        pump_three.value(1)
        sleep(0)
        pump_three_total += seedling_ml
        pump_three.value(0)
    elif toggle_two.value() == 1 | toggle_three.value() == 1:  
        pump_one.value(1)
        sleep(1)
        pump_one_total += veg_mililiters
        pump_one.value(0)
        pump_two.value(1)
        sleep(1)
        pump_two_total += veg_mililiters
        pump_two.value(0)
        pump_three.value(1)
        sleep(1)
        print("hi")
        pump_three_total += veg_mililiters
        pump_three.value(0)
    elif toggle_four.value() == 1:
        pump_one.value(0)
        pump_two.value(0)
        pump_three.value(0)
    elif toggle_five.value() == 1:
        print("manual watering")
    
    # recursion
    water_timer = Timer(period=172_800_000, mode=Timer.ONE_SHOT, callback=fertilizer)  # timer to water every other day


def fertilizer(t):
    """Function that controls the dispensing of liquid fertilizers"""
    
    # global toggle switch state
    global toggle_one, toggle_two, toggle_three, toggle_four, toggle_five
    
    # global pump control
    global fert_one, fert_two, fert_three
    
    # global dispensed amounts
    global fert_one_total, fert_two_total, fert_three_total, stir_plate
    
    # each pump is calibrated to always dispense a certain amount based off current phase per duty cycle
    veg_mililiters = 250
    seedling_ml = 10
    
    # same logic as water_plants()
    if toggle_one.value() == 1:
        stir_plate.value(1)
        sleep(20)
        stir_plate.value(0)
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
        fert_one.value(0)
        fert_two.value(0)
        pump_three.value(0)
    
    fert_timer = Timer(period=172_800_000, mode=Timer.ONE_SHOT, callback=water_plants)  # timer to water every other day

    
def display_lcd(t):
    """Timed function that transmits data to LCDs"""
    
    # hex addresses for lcd(s)
    # SDA(8) SCL(9)
    lcd_one = 0x23  # temperature f
    lcd_two = 0x25  # temperature c
    lcd_three = 0x26  # humidity
    lcd_four = 0x27  # lights
    
    global send_hum, send_temp_c, send_temp_f, low_hum, low_temp_f, low_temp_c, light_time_on, light_time_off, grow_cycle, display_timer
    
    lcd(lcd_one, str(send_temp_f), str(low_temp_f), 1)
    lcd(lcd_two, str(send_temp_c), str(low_temp_c), 2)
    lcd(lcd_three, str(send_hum), str(low_hum), 3) 
    lcd(lcd_four, str(light_time_on), str(light_time_off), 4, str(grow_cycle)) 
    
    display_timer 

# toggle switch GPIO
toggle_one = Pin(16, Pin.IN, Pin.PULL_DOWN)
toggle_two = Pin(17, Pin.IN, Pin.PULL_DOWN)
toggle_three = Pin(18, Pin.IN, Pin.PULL_DOWN)
toggle_four = Pin(19, Pin.IN, Pin.PULL_DOWN)
toggle_five = Pin(6, Pin.IN, Pin.PULL_DOWN)


# global variables for switches
phase_one = False
phase_two = False
phase_three = False
phase_four = False
system_monitoring = False
    
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
pump_one = Pin(15, Pin.OUT)
pump_two = Pin(14, Pin.OUT)
pump_three = Pin(13, Pin.OUT)
fert_one = Pin(20, Pin.OUT)
fert_two = Pin(21, Pin.OUT)
fert_three = Pin(22, Pin.OUT)
stir_plate = Pin(12, Pin.OUT)
send_hum = 0
send_temp_c = 0
send_temp_f = 0

# variables to start water and light cycles
display_timer = Timer(period=30_000, mode=Timer.ONE_SHOT, callback=display_lcd) 
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

    # flash led so user knows system is monitoring
    system_led = Pin(25, Pin.OUT)
    system_led.value(1)
    while True:  # change to number of plants
        while toggle_one.value() == 1:
            print("seedling phase")
            system_monitoring = True
            main_body(toggle_one)
        while toggle_two.value() == 1:
            print("vegetation stage")
            system_monitoring = True
            main_body(toggle_two)
        while toggle_three.value() == 1:
            print("flowering phase")
            system_monitoring = True
            main_body(toggle_three)
        while toggle_four.value() == 1:
            print("harvesting")
            system_monitoring = True
            main_body(toggle_four)
        