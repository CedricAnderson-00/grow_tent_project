# main control for monitoring grow

import grow_tent_main
import grow_tent_main.TempHumiditySensor
from grow_tent_main.views.LcdDisplay import lcd
from grow_tent_main.MySQL.mysql_main import database

test = str((grow_tent_main.TempHumiditySensor.temp_f))
humidity = str((grow_tent_main.TempHumiditySensor.hum))

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