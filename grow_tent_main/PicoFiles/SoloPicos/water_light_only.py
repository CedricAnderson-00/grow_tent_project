from machine import Pin, Timer
from time import sleep


def lights_on(t):
    """lights_on() turns tent light on and then waits a user-defined amount of time. 
       Adds time off to the global variable. After Timer is complete, calls lights_off()
       """
    
    global light
    
    try:
        light.value(1)
        sleep(0.01)
        large_timer_off = Timer(period=64_800_000, mode=Timer.ONE_SHOT, callback=lights_off)  # 18 hours in ms
        Timer.deinit(flower_timer_on)
        Timer.deinit(flower_timer_off)
        
    except: NameError

def lights_off(t):
    """lights_off() turns tent light off and then waits a user-defined amount of time. 
       Adds time on to the global variable. After Timer is complete, calls lights_on()
       """
       
    global light
    
    light.value(0)
    sleep(0.01)
    large_timer_on = Timer(period=21_600_000, mode=Timer.ONE_SHOT, callback=lights_on)  # 6 hours in ms
    
    
def water_plants(t):
    """Function to water each plant for a set amount of time depending on calibration.
       Uses recurrsion to start a timer to repeat in 48 hours
       """
        
    # global GPIO control   
    global water

    water.value(1)
    sleep(55)
    water.value(0)
    
    # recursion timer
    water_timer_switch = Timer(period=43_200_000, mode=Timer.ONE_SHOT, callback=water_plants)  # timer to every 12hrs


def flower_light_off(t):
    """ Function that switches light schedule to 12/12 """
    
    try:
        global light, large_timer_on, large_timer_off
        light.value(0)
        sleep(0.01)
        flower_timer_on = Timer(period=43_200_000, mode=Timer.ONE_SHOT, callback=flower_light_on)  # 12 hours in ms
        Timer.deinit(large_timer_on)
        Timer.deinit(large_timer_off)
    except: NameError

def flower_light_on(t):
    """ Function that turns lights on for 12/12 light schedule """
    global light
    light.value(1)
    flower_timer_off = Timer(period=43_200_000, mode=Timer.ONE_SHOT, callback=flower_light_off)  # 12 hours in ms
    

def main_loop():
    """ Main loop that monitors flowering switch to change cycles """
    
    while flowering_light.value() != 1:

        led_onboard.toggle()
        if manual_water.value() == 1:
            water.value(1)
            sleep(10)
            water.value(0)
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
            flower_light_off(1)
            while flowering_light.value() == 1:
                led_onboard.toggle()
                if manual_water.value() == 1:
                    water.value(1)
                    sleep(10)
                    water.value(0)
                sleep(0.5)
            
        # Turn lights on after flowering phase    
        lights_on(1)
    
# assign GPIO pin locations
manual_water = Pin(2, Pin.IN, Pin.PULL_DOWN)
flowering_light = Pin(15, Pin.IN, Pin.PULL_DOWN)
water = Pin(1, Pin.OUT)
light = Pin(0, Pin.OUT)
led_onboard = Pin(25, Pin.OUT)

# Turn lights on at 18/6 and water plants
lights_on(1)
water_plants(1)

# while loop to enter system monitoring
#will not stop program because flowering switch is off
while True:
    
    while flowering_light.value() != 1:
        main_loop()
        
