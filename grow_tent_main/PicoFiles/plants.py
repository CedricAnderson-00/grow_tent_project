# file to create instances for each plant

class Plants:
    
    # Class attribute
    species = "Cannabis"
    
    def __init__(self, id, temp_f, temp_c, light_on, light_off, hum, soil, water):
        self.id = id
        self.temp_f = temp_f
        self.temp_c = temp_c
        self.light_on = light_on
        self.light_off = light_off
        self.hum = hum
        self.soil = soil
        self.water = water

# create instances with zero values for the amount of plants growing
# writing it here requires less code while program is running    
plant1 = Plants(0, 0, 0, 0, 0, 0, 0, 0)
plant2 = Plants(0, 0, 0, 0, 0, 0, 0, 0)
plant3 = Plants(0, 0, 0, 0, 0, 0, 0, 0)