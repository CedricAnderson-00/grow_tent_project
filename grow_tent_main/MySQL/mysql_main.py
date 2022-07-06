# boilerplate code to establish a connection
# needs to run as soon as program starts

from getpass import getpass
from mysql.connector import connect, Error

# find a way to leave the database open and just add to tables
# create a function that takes a dictionary and adds it to the database
def database(dictionary):
    try:
        with connect(
            host="localhost",
            user="cedric",  # remove prior to sharing
            password="Falconview_3141",  # remove prior to sharing
            database="grow_tent_testing"
        ) as connection:
            plant_id = 2
            temp_f = 8.3
            temp_c = 1.2
            humidity = 37
            test_data = [(plant_id, temp_f, temp_c, humidity)]
            
            # the <%s> tells python that more data will come after the execution of that line
            insert_main_data = """
            INSERT INTO grow_data 
            (id, temp_f, temp_c, humidity)
            VALUES (%s, %s, %s, %s) 
            """
            with connection.cursor() as cursor:
                cursor.executemany(insert_main_data, test_data)  # change to .execute for one arguement
                connection.commit()
    except Error as e:
        print(e)
