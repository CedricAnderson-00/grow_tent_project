# initial test to see if readings will display

import time
import machine
import busio
from adafruit_seesaw.seesaw import Seesaw

print("library loaded")

# setup variables for sampling
sleep_timer = 2.0
deep_sleep = 90
samples = 3
# setup for soil sensor
i2c = busio.I2C(scl=machine.GP1, sda=machine.GP0)
ss = Seesaw(i2c, addr=0x36)




# Configure the RP2040 Pico LED Pin as an output
led_pin = DigitalInOut(machine.LED)
led_pin.switch_to_output()


def avg_soil(sleep_timer, samples):
    print("Soil")
    count = 0
    total = 0
    while count < samples:
        total = total + ss.moisture_read()
        time.sleep(sleep_timer)
        count += 1
    soil = total / samples
    return (round(soil, 2))


while True:
    try:
        print("Moisture:{}".format(avg_soil(sleep_timer, samples)))

    except (ValueError, RuntimeError) as e:
        print("Failed to get data, retrying\n", e)

    response = None
    time.sleep(deep_sleep)