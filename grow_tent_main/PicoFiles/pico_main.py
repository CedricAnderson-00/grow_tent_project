from time import sleep
from machine import Timer, Pin, UART
from TempHumiditySensor import get_temp_hum
from SoilMoistureSensor import soil_sensor_one, soil_sensor_two, soil_sensor_three


# functions
def main_body(switch):
    """Function that sends and receives values from sensors. Takes one arguement that is used to monitor state of toggle switches"""
    
    global low_hum, low_temp_c, low_temp_f, system_timer, system_led, pump_one_total, pump_two_total, pump_three_total, temp_c, temp_f, hum, pump_one
    
    while switch.value() == 1:
        if toggle_five.value() == 1:  # manual water
            pump_one.value(1)
            sleep(10)
            pump_one.value(0)  
        uart = UART(0, 115200)
        system_led.toggle()
        water_plants()
        light_controller()
        tent_environment()
        database()

        # transfer values in tent state to master Pi
        if uart.any() == 1:
            plant = 1, temp_f, temp_c, hum, system_timer, pump_one_total
            uart.write(str(plant).encode('utf-8'))
            sleep(0.01)  # this depends on how much data is sent
            pump_one_total = 0    
            
        elif uart.any() == 2:
            plant = 2, temp_f, temp_c, hum, system_timer, pump_two_total
            uart.write(str(plant).encode('utf-8'))
            sleep(0.01)  # this depends on how much data is sent
            pump_two_total = 0       

        elif uart.any() == 3:
            plant = 3, temp_f, temp_c, hum, system_timer, pump_three_total
            uart.write(str(plant).encode('utf-8'))
            sleep(0.01)  # this depends on how much data is sent
            pump_three_total = 0
                
                
def system_controller(t):
    """Function that adds 1 hour to system timer to control time based processes"""
    
    global system_timer
    
    system_timer += 1
    

def light_controller():
    """Function that turns on/off tent lights based on system time"""
    
    global system_timer, tent_light_control, light_redundancy_check
    
    if toggle_one.value() == 1:
        if system_timer == 12:
            if light_redundancy_check == 0:
                tent_light_control.value(1)
                light_redundancy_check += 1
        if system_timer == 24:
            if light_redundancy_check == 1:
                tent_light_control.value(1)
                light_redundancy_check = 0
                system_timer = 0
    if toggle_two.value() == 1:
        if system_timer == 12:
            if light_redundancy_check == 0:
                tent_light_control.value(1)
                light_redundancy_check += 1
        if system_timer == 24:
            if light_redundancy_check == 1:
                tent_light_control.value(1)
                light_redundancy_check = 0
                system_timer = 0
    if toggle_three.value() == 1:
        if system_timer == 12:
            if light_redundancy_check == 0:
                tent_light_control.value(0)
                light_redundancy_check += 1
        if system_timer == 24:
            if light_redundancy_check == 1:
                tent_light_control.value(1)
                light_redundancy_check = 0
                system_timer = 0
    if toggle_four.value() == 1:
        if system_timer == 12:
            if light_redundancy_check == 0:
                tent_light_control.value(0)
                light_redundancy_check += 1
        if system_timer == 24:
            if light_redundancy_check == 1:
                tent_light_control.value(0)
                light_redundancy_check = 0
                system_timer = 0
       
    
def water_plants():
    """Function that uses system time to water plants at 12 hour intervals"""
        
    # global GPIO control   
    global pump_one, system_timer, water_redundancy_check
    
    # global dispensed values
    global pump_one_total, pump_two_total, pump_three_total

    if toggle_one.value() == 1:
        if system_timer == 12:
            if water_redundancy_check == 0:
                pump_one.value(1)
                sleep(3)
                pump_one.value(0)
                pump_one_total += 500
                pump_two_total += 500
                pump_three_total += 500
                water_redundancy_check += 1
        if system_timer == 24:
            if water_redundancy_check == 1:
                pump_one.value(1)
                sleep(2)
                pump_one.value(0)
                water_redundancy_check = 0
    if toggle_two.value() == 1:
        if system_timer == 12:
            if water_redundancy_check == 0:
                pump_one.value(1)
                sleep(55)
                pump_one.value(0)
                pump_one_total += 500
                pump_two_total += 500
                pump_three_total += 500
                water_redundancy_check += 1
        if system_timer == 24:
            if water_redundancy_check == 1:
                pump_one.value(1)
                sleep(25)
                pump_one.value(0)
                pump_one_total += 500
                pump_two_total += 500
                pump_three_total += 500
                water_redundancy_check = 0
    if toggle_three.value() == 1:
        if system_timer == 12:
            if water_redundancy_check == 0:
                pump_one.value(1)
                sleep(55)
                pump_one.value(0)
                pump_one_total += 500
                pump_two_total += 500
                pump_three_total += 500
                water_redundancy_check += 1
        if system_timer == 24:
            if water_redundancy_check == 1:
                pump_one.value(1)
                sleep(55)
                pump_one.value(0)
                pump_one_total += 500
                pump_two_total += 500
                pump_three_total += 500
                water_redundancy_check = 0
    if toggle_four.value() == 1:
        if system_timer == 12:
            if water_redundancy_check == 0:
                water_redundancy_check += 1
        if system_timer == 24:
            if water_redundancy_check == 1:
                water_redundancy_check = 0
    

def database():
    """Function that creates a .txt file to store system time.
       Reads data from file to continue system_timer
       """
    
    global system_timer, counter, light_redundancy_check, tent_light_control, database_values, light_value_database

    # avoids reading the file after system startup
    if counter == 0:
        file = open("database.txt","r")
        database = str(file.read())
        database_values = database.split(", ")
        file.close()
        counter += 1
    if counter >= 1:
        file = open("database.txt","w")
        light_value_database = tent_light_control.value()
        file.write(str(system_timer) + ", ")
        file.write(str(light_redundancy_check) + ", ")
        file.write(str(light_value_database))
        file.close()


def tent_environment():
    """Function that controls the temperature and humidity environment of the grow tent."""
    
    global temp_c, temp_f, hum
    
    x = get_temp_hum()
    temp_c = x[0]
    hum = x[2]
    temp_f = x[1]

    # logic to test current state of system
    if temp_f > 85:
        heat_control.value(0)
        sleep(0.01)
        if temp_f > 88:
            exhaust.value(1)
    elif temp_f < 84:  # the gap in temp_c is to reduce wear on relay
        exhaust.value(0)
        sleep(0.01)
        if temp_f < 78:
            heat_control.value(1)
            sleep(0.01)

    # this logic will check humidity levels and operate relay
    if hum > 55:
        hum_control.value(0)
        sleep(0.01)
        dehumidifier.value(0)
        sleep(0.01)
        if hum >= 63:
            dehumidifier.value(1)
            sleep(0.01)
            hum_control.value(0)
            sleep(0.01)
    elif hum < 50:
        hum_control.value(1)
        sleep(0.01)
        dehumidifier.value(0)
        sleep(0.01)


# toggle switch GPIO
toggle_one = Pin(16, Pin.IN, Pin.PULL_DOWN)
toggle_two = Pin(17, Pin.IN, Pin.PULL_DOWN)
toggle_three = Pin(18, Pin.IN, Pin.PULL_DOWN)
toggle_four = Pin(19, Pin.IN, Pin.PULL_DOWN)
toggle_five = Pin(6, Pin.IN, Pin.PULL_DOWN)

# timer values 
system_timer = 0
counter = 0
light_time_off = 0
pump_one_total = 0
pump_two_total = 0
pump_three_total = 0
water_redundancy_check = 0
light_redundancy_check = 0
database_values = []

# GPIO assignments
tent_light_control = Pin(12, Pin.OUT)
pump_one = Pin(15, Pin.OUT)  # water
pump_two = Pin(14, Pin.OUT)  # fertilizer
pump_three = Pin(13, Pin.OUT)
fert_one = Pin(20, Pin.OUT)
fert_two = Pin(21, Pin.OUT)
fert_three = Pin(22, Pin.OUT)
stir_plate = Pin(13, Pin.OUT)
dehumidifier = Pin(19, Pin.OUT)
heat_control = Pin(16, Pin.OUT)
exhaust = Pin(18, Pin.OUT)
hum_control = Pin(17, Pin.OUT)
led_onboard = Pin(25, Pin.OUT)

# variables to start water and light cycles
timer_one = Timer(period=3_600_000, mode=Timer.PERIODIC, callback=system_controller)

# low values
# set to maximum values for initial running of program to establish low values
temp_f = 212
temp_c = 100
hum = 100
grow_cycle = 0

# ensure all relays are off at the start of program
dehumidifier.value(0)
hum_control.value(0)
heat_control.value(0)
exhaust.value(0)

# establish system time
database()

# Assign values from database() to respected variable
system_timer = int(database_values[0])
water_redundancy_check = int(database_values[1])
light_redundancy_check = int(database_values[1])
initial_light_reading = int(database_values[2])
tent_light_control.value(initial_light_reading)

# close .txt file
database()

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
            main_body(toggle_three)
        while toggle_four.value() == 1:
            main_body(toggle_four)
