import utime
import machine

# set GPIO pins
start_sensor = machine.Pin(28, machine.Pin.IN, machine.Pin.PULL_DOWN)
uart = machine.UART(0, 115200)

# loop that executes once power is supplied to GPIO28
def signal_received():
    counter = 0
    while counter:
        
    led_onboard = machine.Pin(25, machine.Pin.OUT)
    led_onboard.value(1)
    
    # variable 
    y = "This means that it completed the loop!!"
    
    # transmit to master Pico
    uart.write(y)

# monitore signals through IRQ
start_sensor.irq(trigger=machine.Pin.IRQ_RISING, handler=signal_received)