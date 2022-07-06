# main control for monitoring grow

import grow_tent_main
import grow_tent_main.TempHumiditySensor
from grow_tent_main.views.LcdDisplay import lcd
from grow_tent_main.MySQL.mysql_main import connect

test = str((grow_tent_main.TempHumiditySensor.temp_f))
humidity = str((grow_tent_main.TempHumiditySensor.hum))

# empty dictionary to send to database
sql_dict = {'plant_id': 1, 'temp_f': 00.0, 'temp_c': 00.0, 'humidity': 00,
            'daily_water': 00.0, 'light_on': 00.00, 'light_off': 00.00, 
            'soil_moisture': 000, 'soil_ph': 000.000}

# print to lcd display
# must convert to string prior to this step
# the current LCD can only take a length of 16/line currently spaced
# find a more efficient way to print each line
lcd(f"Temp: {test} F    Humidity: {humidity}")