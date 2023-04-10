from time import sleep
import serial
from MySQL.mysql_main import database

def receive_from_Pico(value):
    """Function that takes an argument the represents a length.
       Passes the length value to Pi Pico to send the corresponding plant values"""
    try:
        ser = serial.Serial(
        port = '/dev/ttyS0',  # Change this according to connection methods, e.g. /dev/ttyUSB0
        baudrate = 115200,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
        )
        
        print("Gathering data.....")    
        ser.write(value.encode('utf-8'))
        from_pico = ser.readline()
        decode_pico = from_pico.decode()
        print(decode_pico)
        x = decode_pico.strip("()")
        new_list = list(x.split(","))
    except IndexError:
        print("check sent data from pico")
    
    return new_list
    
while True:
    try:
        # receive values from Pico
        plant1 = receive_from_Pico("1")
        plant2 = receive_from_Pico("1.")
        plant3 = receive_from_Pico("1..")
        plant4 = receive_from_Pico("1...")
        
        # send values to database
        database(plant1)
        database(plant2)
        database(plant3)
        database(plant4)
        
        sleep(3_600)  # sleep for one hour
    except IndexError:
        print("check sent data from pico")
    except OSError:
        print("memory issue")
