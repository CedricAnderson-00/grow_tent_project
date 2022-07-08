# main control for monitoring grow

import grow_tent_main
import grow_tent_main.PicoFiles.TempHumiditySensor
from grow_tent_main.views.LcdDisplay import lcd
from grow_tent_main.MySQL.mysql_main import database
import time
import serial


ser = serial.Serial(
  port='/dev/ttyS0', # Change this according to connection methods, e.g. /dev/ttyUSB0
  baudrate = 115200,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=1
)

# loop to collect values throughout the day
#  add try / except statements to prevent crash
while True:
    print("Gathering Readings.....")
    ser.write('start'.encode('utf-8'))
    time.sleep(2)
    from_pico = ser.readline()
    decode_pico = from_pico.decode('utf-8')
    print(decode_pico)  # a for loop is needed here to strip and convert values to INT
    time.sleep(2)

# empty list to send to database
sql_list = [
    75.2
]

# test the input of large file into database
database(sql_list)

# print to lcd display
# must convert to string prior to this step
# the current LCD can only take a length of 16/line currently spaced
# find a more efficient way to print each line
# lcd(f"Temp: {test} F    Humidity: {humidity}")