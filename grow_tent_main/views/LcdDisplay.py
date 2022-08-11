# module to display content

import utime

import machine
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

# lcd properties
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

def lcd(hex_address, value):
    """Receives a hex address and a value to display"""
    
    # display value
    i2c = I2C(0, sda=machine.Pin(8), scl=machine.Pin(9), freq=400000)  # can listen on different i2c pin by changing <0>
    lcd = I2cLcd(i2c, hex_address, I2C_NUM_ROWS, I2C_NUM_COLS)    
    lcd.putstr(value)
    
    return
   