# main control for monitoring grow

import grow_tent_main
import grow_tent_main.TempHumiditySensor
from grow_tent_main.views.LcdDisplay import lcd

test = str((grow_tent_main.TempHumiditySensor.temp_f))
humidity = str((grow_tent_main.TempHumiditySensor.hum))

# print to lcd display
# must convert to string prior to this step
# the current LCD can only take a length of 16/line currently spaced
# find a more efficient way to print each line
lcd(f"Temp: {test} F    Humidity: {humidity}")