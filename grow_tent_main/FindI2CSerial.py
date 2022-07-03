# run this code to find the address of device connected to I2C

import machine
sda = machine.Pin(0)
scl = machine.Pin(1)
i2c = machine.I2C(0, sda=sda, scl=scl, freq=400000)  # change Pin(0) location to desired pin location
print(i2c.scan())