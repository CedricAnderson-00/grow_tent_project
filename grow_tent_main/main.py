import time
import serial

def receive_from_Pico(value):
    ser = serial.Serial(
    port='/dev/ttyS0', # Change this according to connection methods, e.g. /dev/ttyUSB0
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
    decode_pico.strip("(", ")")
    
    return decode_pico
    
plant1 = receive_from_Pico("1")
plant2 = receive_from_Pico("1.")
plant3 = receive_from_Pico("1..")

# # empty list to send to database
# sql_list = [
#     75.2
# ]

# # test the input of large file into database
# database(sql_list)

# print to lcd display
# must convert to string prior to this step
# the current LCD can only take a length of 16/line currently spaced
# find a more efficient way to print each line
# lcd(f"Temp: {test} F    Humidity: {humidity}")