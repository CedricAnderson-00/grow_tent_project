# boilerplate code to establish a connection
# needs to run as soon as program starts

from getpass import getpass
from mysql.connector import connect, Error
from datetime import datetime

# find a way to leave the database open and just add to tables
# create a function that takes a dictionary and adds it to the database
def database(list):
    try:
        with connect(
            host="localhost",
            user="cedric",  # remove prior to sharing
            password="Falconview_3141",  # remove prior to sharing
            database="grow_tent_testing"
        ) as connection:
            plant_id = list[8]
            temp_f = list[0]
            temp_c = list[1]
            humidity = list[2]
            daily_water = list[3]
            light_on = list[4]
            light_off = list[5]
            soil_moisture = list[6]
            soil_ph = list[7]
            first_flower = datetime.now()
            test_data = [(temp_f, temp_c, humidity, daily_water, light_on, light_off, 
                          soil_moisture, soil_ph, first_flower, plant_id)]
            
            # the <%s> tells python that more data will come after the execution of that line
            insert_main_data = """
            INSERT INTO grow_values 
                (temp_f, temp_c, humidity, daily_water, light_on, light_off, 
                soil_moisture, soil_ph, first_flower, plant_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
            """
            with connection.cursor() as cursor:
                cursor.executemany(insert_main_data, test_data)  # change to .execute for one arguement
                connection.commit()
                print("complete")
    except Error as e:
        print(e)