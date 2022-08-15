# boilerplate code to establish a connection
# needs to run as soon as program starts

from getpass import getpass
from mysql.connector import connect, Error
from datetime import datetime

# find a way to leave the database open and just add to tables
# create a function that takes a dictionary and adds it to the database
def database(list):
    """Function that takes a list as an arguement. Inserts values into database
       by their index locations."""
    
    try:
        with connect(
            host = "localhost",
            user = "user",  # remove prior to sharing
            password = "password",  # remove prior to sharing
            database = "grow_tent_testing"
        ) as connection:
            plant_id = list[0]
            temp_f = list[1]
            temp_c = list[2]
            humidity = list[5]
            daily_water = list[7]
            fert_water = list[8]
            light_on = list[3]
            light_off = list[4]
            soil_moisture = list[6]
            program_time = datetime.now()
            test_data = [(temp_f, temp_c, humidity, daily_water, fert_water, light_on, light_off, 
                          soil_moisture, program_time, plant_id)]
            
            # the <%s> tells python that more data will come after the execution of that line
            insert_main_data = """
            INSERT INTO grow_values 
                (temp_f, temp_c, humidity, daily_water, fert_water, light_on, light_off, 
                soil_moisture, program_time, plant_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
            """
            with connection.cursor() as cursor:
                cursor.executemany(insert_main_data, test_data)  # change to .execute for one arguement
                connection.commit()
                print("complete")
    except Error as e:
        print(e)