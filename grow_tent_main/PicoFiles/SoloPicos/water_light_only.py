from machine import Pin, Timer
from time import sleep


def system_controller(t):
    """Function that adds 1 hour to system timer to control time based processes"""
    
    global system_timer
    
    system_timer += 1


def light_controller():
    """function that monitors system_timer to control the light state. Only used when flowering_light is '0'
       """
    
    global light, system_timer, light_redundancy_check
    
    if flowering_light.value() == 0:
        if system_timer == 18:
            if light_redundancy_check == 0:
                light.value(0)
                light_redundancy_check += 1
        if system_timer >= 24:
            if light_redundancy_check == 1:
                light.value(1)
                light_redundancy_check = 0
                system_timer = 0
               

def water_plants():
    """Function that uses system time to water plants at 12 hour intervals"""
        
    # global GPIO control   
    global water, system_timer, water_redundancy_check
    
    if flowering_light.value() == 0:
        if system_timer == 12:
            if water_redundancy_check == 0:
                water.value(1)
                sleep(25)
                water.value(0)
                water_redundancy_check += 1
        if system_timer >= 24:
            if water_redundancy_check == 1:
                water_redundancy_check = 0


def flowering_water_plants():
    """Function that uses system time to water plants at 12 hour intervals"""
        
    # global GPIO control   
    global water, system_timer, water_redundancy_check

    if system_timer == 12:
        if water_redundancy_check == 0:
            water.value(1)
            sleep(55)
            water.value(0)
            water_redundancy_check += 1
    if system_timer >= 24:
        if water_redundancy_check == 1:
            water_redundancy_check = 0


def flowering_light_control():
    """Function that turns on/off tent lights based on system time"""
    
    global system_timer, tent_light_control, light_redundancy_check
    
    if system_timer == 12:
        if light_redundancy_check == 0:
            tent_light_control.value(1)
            light_redundancy_check += 1
    if system_timer >= 24:
        if light_redundancy_check == 1:
            tent_light_control.value(0)
            light_redundancy_check = 0
            system_timer = 0


def database():
    """Function that creates a .txt file to store system time.
       Reads data from file to continue system_timer
       """
    
    global file, system_timer, counter
    
    # avoids reading the file after system startup
    if counter == 0:
        file = open("database.txt","r")
        system_timer = int(file.read())
        file.close()
        counter += 1
    if counter >= 1:
        file = open("database.txt","w")
        file.write(str(system_timer))
        file.close()


def main_loop():
    """ Main loop that monitors flowering switch to change cycles """
    
    while flowering_light.value() != 1:

        led_onboard.toggle()
        water_plants()
        light_controller()
        database()
        if manual_water.value() == 1:
            water.value(1)
            sleep(10)
            water.value(0)
            water_plants()
        sleep(0.5)
        
    if flowering_light.value() == 1:
        
        # countdown to abort flowering phase
        led_onboard.value(1)
        sleep(1)
        led_onboard.value(0)
        sleep(1)
        led_onboard.value(1)
        sleep(1)
        led_onboard.value(0)
        sleep(1)
        led_onboard.value(1)
        sleep(1)
        led_onboard.value(0)
        
        # start flowering phase
        if flowering_light.value() == 1:
            while flowering_light.value() == 1:
                led_onboard.toggle()
                flowering_water_plants()
                flowering_light_control()
                database()
                if manual_water.value() == 1:
                    water.value(1)
                    sleep(10)
                    water.value(0)
                sleep(0.5)
            
        # Turn lights on after flowering phase    
        light.value(1)
    
# assign GPIO pin locations
manual_water = Pin(2, Pin.IN, Pin.PULL_DOWN)
flowering_light = Pin(15, Pin.IN, Pin.PULL_DOWN)
water = Pin(1, Pin.OUT)
light = Pin(0, Pin.OUT)
led_onboard = Pin(25, Pin.OUT)

# establish initial values for system
counter = 0
system_timer = 0
water_redundancy_check = 1
light_redundancy_check = 1

# get values from database()
database()
light.value(1)

# Turn lights on at 18/6 and water plants
timer_one = Timer(period=3_600_000, mode=Timer.PERIODIC, callback=system_controller)


# while loop to enter system monitoring
#will not stop program because flowering switch is off
while True:
    
    while flowering_light.value() != 1:
        main_loop()
        
