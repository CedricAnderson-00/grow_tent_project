# module to display content

import utime

import machine
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

I2C_ADDR     = 0x27  # be sure to run the sample code in /FindI2CSerial.py to find device address. Convert value to hex
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

def lcd(value):
    """Receives any value to display on LCD"""
    
    #Test function for verifying basic functionality
    i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)  # can add multiple LCDs by changing serial ID (0)
    lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)    
    lcd.putstr(value)
    
    return
    