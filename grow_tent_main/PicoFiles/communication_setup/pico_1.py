# receiver.py / Tx/Rx => Tx/Rx
# connection between Raspberry Pi and Pico

import os
import machine
import utime


# port to establish connection
uart = machine.UART(0, 115200)
uart_1 = machine.UART(1, 115200)

# GPIO pin to pico_2
start = machine.Pin(15, machine.Pin.OUT)

# to notify user that the program is running
# this will be moved into loop boody once program format is complete
print("*****Program running*****")

while True:
    print("waiting")
    utime.sleep(1)
    if uart.any():
        start.value(1)
        utime.sleep(5)
        received_byte = uart.read(20)
        uart.write(str(received_byte))  # only know how to send strings through UART connection