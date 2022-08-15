# change to main.py when ready to upload to Pico
# monitors and controls the activation of heating elements.

from machine import Pin, Timer
from time import sleep
import dht
from LcdDisplay import lcd


def display_lcd(t):
    """Timed function that transmits data to LCDs"""

    # hex addresses for lcd(s)
    # SDA(8) SCL(9)
    lcd_one = 0x23  # temperature f
    lcd_two = 0x25  # temperature c
    lcd_three = 0x26  # humidity
    lcd_four = 0x27  # lights

    global hum, temp, temp_f, low_hum, low_temp_f, low_temp_c, light_time_on, light_time_off

    lcd(lcd_one, str(temp_f), str(low_temp_f), 1)
    lcd(lcd_two, str(temp), str(low_temp_c), 2)
    lcd(lcd_three, str(hum), str(low_hum), 3)
    #lcd(lcd_four, str(light_time_on), str(light_time_off), 4, str(grow_cycle))


# assign GPIO pin locations
# emergency_cooling = Pin(18, Pin.OUT)
dehumidifier = Pin(19, Pin.OUT)
heat_control = Pin(16, Pin.OUT)
hum_control = Pin(17, Pin.OUT)
sensor = dht.DHT11(Pin(6))
led_onboard = Pin(25, Pin.OUT)

# set high to ensure a reasonable low value is set
low_temp_c = 100
low_temp_f = 212
low_hum = 100

# ensure all relays are off at the start of program
dehumidifier.value(0)
hum_control.value(0)
heat_control.value(0)

# start display timer to display values every minute
display_timer = Timer(period=10_000, mode=Timer.PERIODIC, callback=display_lcd)

# while loop to continuosly monitor system
while True:
    try:
        led_onboard.toggle()
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        temp_f = temp * (9 / 5) + 32

        # logic to test current state of system
        if temp_f == 80:
            heat_control.value(0)
            # emergency_cooling.value(0)
        elif temp_f > 85:
            heat_control.value(0)
        elif temp_f < 78.5:  # the gap in temp is to reduce wear on relay
            heat_control.value(1)

        # this logic will check humidity levels and operate relay
        if hum == 50:
            hum_control.value(0)
            dehumidifier.value(0)
        elif hum >= 55:
            dehumidifier.value(1)
            hum_control.value(0)
        elif hum < 46:
            hum_control.value(1)
            dehumidifier.value(0)

        # logic to get low and high values
        if hum < low_hum:
            low_hum = hum

        if temp < low_temp_c:
            low_temp_c = temp

        if temp_f < low_temp_f:
            low_temp_f = temp_f

        sleep(0.2)  

    except (OSError, TypeError):
        print("no reading from sensor")
        heat_control.value(0)
        hum_control.value(0)
