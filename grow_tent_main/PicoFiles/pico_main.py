# receiver.py / Tx/Rx => Tx/Rx
import os
import machine
from time import sleep
from main import from_pi

uart = machine.UART(0, 115200)

b = None
msg = ""

print("*****Program running*****")

while True:
    print(".")
    sleep(1)
    if uart.any():
        x = from_pi()
        uart.write(str(x))