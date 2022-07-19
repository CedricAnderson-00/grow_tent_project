from time import sleep
import serial
from MySQL.mysql_main import database

def receive_from_Pico(value):
    """Function that takes an argument the represents a length.
       Passes the length value to Pi Pico to send the corresponding plant values"""
    
    ser = serial.Serial(
    port='/dev/ttyS0',  # Change this according to connection methods, e.g. /dev/ttyUSB0
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
    )
    
    print("Gathering data.....")    
    ser.write(value.encode('utf-8'))
    from_pico = ser.readline()
    decode_pico = from_pico.decode()
    print(decode_pico)
    x = decode_pico.strip("()")
    new_list = list(x.split(","))
    
    return new_list
    
while True:
    # receive values from Pico
    plant1 = receive_from_Pico("1")
    plant2 = receive_from_Pico("1.")
    plant3 = receive_from_Pico("1..")
    
    # send values to database
    database(plant1)
    database(plant2)
    database(plant3)
    
    sleep(1_800_000)  # sleep for one hour


# print to lcd display
# must convert to string prior to this step
# the current LCD can only take a length of 16/line currently spaced
# find a more efficient way to print each line
# lcd(f"Temp: {test} F    Humidity: {humidity}")