from machine import I2C
from pico_i2c_lcd import I2cLcd

# lcd properties
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

def lcd(hex_address, value_1, value_2, name, *args):
    """Receives a hex address and a value to display"""
      
    # display value
    i2c = I2C(0, sda=machine.Pin(8), scl=machine.Pin(9), freq=400000)  # can listen on different i2c pin by changing <0>
    lcd = I2cLcd(i2c, hex_address, I2C_NUM_ROWS, I2C_NUM_COLS)
    if name == 1:    
        lcd.putstr(f"Temperature F \nH: {value_1:.4}  L: {value_2:.4}")
    elif name == 2:
        lcd.putstr(f"Temperature C \nH: {value_1:.4} L: {value_2:.4}")
    elif name == 3:
        lcd.putstr(f"Humidity \nH: {value_1:.4} L: {value_2:.4}")
    elif name == 4:
        lcd.putstr(f"Light On: {value_1}h\nOff: {value_2}h P: {args[0]}")
    
    return
