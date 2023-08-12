from time import sleep
from machine import Timer, Pin, UART, PWM
from TempHumiditySensor import get_temp_hum
from LcdDisplay import lcd

try:
    # functions
    def main_body(switch):
        """Function that sends and receives values from sensors. Takes one arguement that is used to monitor state of toggle switches"""

        global system_timer, system_led, dispensed_water_total, temp_c, temp_f, hum, relay_4, error_counter
        try:
            while switch.value() == 1:
                uart = UART(0, 115200)
                system_led.toggle()
                water_plants()
                light_controller()
                tent_environment()
                database()
                system_reset()

                # transfer values in tent state to master Pi
                if uart.any() == 1:
                    plant = 1, temp_f, temp_c, hum, system_timer, dispensed_water_total
                    uart.write(str(plant).encode('utf-8'))
                    sleep(0.01)  # this depends on how much data is sent

                elif uart.any() == 2:
                    plant = 2, temp_f, temp_c, hum, system_timer, dispensed_water_total
                    uart.write(str(plant).encode('utf-8'))
                    sleep(0.01)  # this depends on how much data is sent

                elif uart.any() == 3:
                    plant = 3, temp_f, temp_c, hum, system_timer, dispensed_water_total
                    uart.write(str(plant).encode('utf-8'))
                    sleep(0.01)  # this depends on how much data is sent
                    dispensed_water_total = 0
        # exception handling for ADT sensor's missed readings
        except (TypeError, ValueError, IndexError):
            error_counter += 1

    def system_controller(t):
        """Function that adds 1 hour to system timer to control time based processes"""

        global system_timer

        system_timer += 1

    def light_controller():
        """Function that turns on/off tent lights based on system time"""

        global system_timer, relay_2, light_redundancy_check

        if toggle_one.value() == 1:
            if system_timer <= 23 and light_redundancy_check == 0:
                relay_2.value(1)
                relay_3.value(1)
                relay_5.value(1)
                light_redundancy_check += 1
            if system_timer == 24 and light_redundancy_check >= 1:
                relay_2.value(1)
                relay_3.value(1)
                relay_5.value(1)
                light_redundancy_check = 0
                system_timer = 0
        if toggle_two.value() == 1:
            if system_timer <= 23 and light_redundancy_check == 0:
                relay_2.value(1)
                relay_3.value(1)
                relay_5.value(1)
                light_redundancy_check += 1
            if system_timer == 24 and light_redundancy_check >= 1:
                relay_2.value(1)
                relay_3.value(1)
                relay_5.value(1)
                light_redundancy_check = 0
                system_timer = 0
        if toggle_three.value() == 1:
            if system_timer == 12 and light_redundancy_check == 0:
                relay_2.value(0)
                relay_3.value(0)
                relay_5.value(0)
                light_redundancy_check += 1
            if system_timer == 24 and light_redundancy_check >= 1:
                relay_2.value(1)
                relay_3.value(1)
                relay_5.value(1)
                light_redundancy_check = 0
                system_timer = 0
        if toggle_four.value() == 1:
            if system_timer <= 23 and light_redundancy_check == 0:
                relay_2.value(0)
                relay_3.value(0)
                relay_5.value(0)
                light_redundancy_check += 1
            if system_timer == 24 and light_redundancy_check >= 1:
                relay_2.value(0)
                relay_3.value(0)
                relay_5.value(0)
                light_redundancy_check = 0
                system_timer = 0

    def water_plants():
        """Function that uses system time to water plants at 12 hour intervals"""

        # global GPIO control
        global relay_4, system_timer, water_redundancy_check

        # global dispensed values
        global dispensed_water_total

        if toggle_one.value() == 1:
            if system_timer == 12 and water_redundancy_check == 0:
                relay_4.value(1)
                sleep(3)
                relay_4.value(0)
                dispensed_water_total += 30
                water_redundancy_check += 1
            if system_timer == 24 and water_redundancy_check >= 1:
                relay_4.value(1)
                sleep(2)
                relay_4.value(0)
                water_redundancy_check = 0
        if toggle_two.value() == 1:
            if system_timer == 23 and water_redundancy_check == 3:
                relay_4.value(1)
                sleep(55)
                relay_4.value(0)
                dispensed_water_total += 550
                water_redundancy_check = 4
            elif water_redundancy_check >= 4 and system_timer >= 24:
                relay_4.value(1)
                sleep(45)
                relay_4.value(0)
                dispensed_water_total += 450
                water_redundancy_check = 0
            elif system_timer == 12:
                if water_redundancy_check == 0:
                    water_redundancy_check += 1
                elif water_redundancy_check == 2:
                    water_redundancy_check += 1
            elif system_timer == 24:
                if water_redundancy_check == 1:
                    water_redundancy_check += 1
        if toggle_three.value() == 1:
            if system_timer == 12 and water_redundancy_check == 0:
                relay_4.value(1)
                sleep(55)
                relay_4.value(0)
                dispensed_water_total += 550
                water_redundancy_check = 1
            if system_timer == 13 and water_redundancy_check >= 1:
                relay_4.value(1)
                sleep(45)
                relay_4.value(0)
                dispensed_water_total += 450
                water_redundancy_check = 0
        if toggle_four.value() == 1:
            if system_timer == 12 and water_redundancy_check == 0:
                    water_redundancy_check += 1
            if system_timer == 24 and water_redundancy_check == 1:
                    water_redundancy_check = 0

    def database():
        """Function that creates a .txt file to store system time.
        Reads data from file to continue system_timer
        """

        global system_timer, counter, light_redundancy_check, relay_2, database_values, light_value_database

        # avoids reading the file after system startup
        if counter == 0:
            file = open("database.txt", "r")
            database = str(file.read())
            database_values = database.split(", ")
            file.close()
            counter += 1
        if counter >= 1:
            file = open("database.txt", "w")
            light_value_database = relay_2.value()
            file.write(str(system_timer) + ", ")
            file.write(str(light_redundancy_check) + ", ")
            file.write(str(water_redundancy_check) + ", ")
            file.write(str(light_value_database))
            file.close()

    def tent_environment():
        """Function that controls the temperature and humidity environment of the grow tent."""

        global relay_8, relay_9, temp_c, temp_f, hum, toggle_one, toggle_two, toggle_three, toggle_four, temp_check_value, humidity_check_value, low_temp_check_value, low_humidity_check_value, sensor

        # check toggle switches to determine what maximum values are.
        if toggle_one.value() == 1:
            temp_check_value         = 97
            low_temp_check_value     = 82
            humidity_check_value     = 65
            low_humidity_check_value = 55
        if toggle_two.value() == 1:
            temp_check_value         = 85
            low_temp_check_value     = 86
            humidity_check_value     = 55
            low_humidity_check_value = 48
        if toggle_three.value() == 1:
            relay_1.value(1)
            temp_check_value         = 78
            low_temp_check_value     = 68
            humidity_check_value     = 50
            low_humidity_check_value = 42
        if toggle_four.value() == 1:
            relay_1.value(1)
            temp_check_value         = 76
            low_temp_check_value     = 72
            humidity_check_value     = 42
            low_humidity_check_value = 38

        x      = get_temp_hum(sensor)
        temp_c = x[0]
        hum    = x[2]
        temp_f = x[1]

        # logic to test current state of system
        if temp_f > temp_check_value:
            relay_8.value(0)
            if temp_f > (temp_check_value + 3):
                relay_9.value(1)
        if temp_f < low_temp_check_value:  # the gap in temp_c is to reduce wear on relay
            relay_9.value(0)
            if temp_f < (low_temp_check_value - 2):
                relay_8.value(1)

        # this logic will check humidity levels and operate relay
        if hum > humidity_check_value:
            relay_6.value(0)
            if hum >= humidity_check_value + 2 and toggle_three.value() != 1 or toggle_four.value() != 1:
                relay_1 .value(1)
                relay_11.value(1)
                relay_12.value(1)
                relay_13.value(1)
                relay_14.value(1)
            else:
                relay_11.value(1)
                relay_12.value(1)
                relay_13.value(1)
                relay_14.value(1)
                
        if hum < low_humidity_check_value and toggle_three.value() != 1 or toggle_four.value() != 1:
            relay_6 .value(1)
            relay_1 .value(0)
            relay_11.value(0)
            relay_12.value(0)
            relay_13.value(0)
            relay_14.value(0)
        else:
            relay_6 .value(1)
            relay_11.value(0)
            relay_12.value(0)
            relay_13.value(0)
            relay_14.value(0)

    def display_lcd(t):
        """Timed function that transmits data to LCDs"""

        global hum, temp_f, temp_c, light_time_off, system_timer, error_counter, water_redundancy_check

        # hex addresses for lcd(s)
        # SDA(8) SCL(9)
        lcd_one = 0x27  # temperature f

        # # reset counter to 0 when over 99
        # if error_counter > 99:
        #     error_counter = 0

        lcd(lcd_one, str(temp_f), str(hum), str(temp_c),
            str(system_timer), str(water_redundancy_check), 1)

    def system_reset():
        """ Function to reset all values to 0 """

        global system_timer, counter, error_counter, water_redundancy_check, light_redundancy_check, dispensed_water_total, light_time_off, light_time_on

        if toggle_one.value() == 1 & toggle_three.value() == 1:
            sleep(5)
            system_timer           = 0
            counter                = 0
            error_counter          = 0
            water_redundancy_check = 0
            light_redundancy_check = 0
            dispensed_water_total  = 0
            light_time_off         = 0
            light_time_on          = 0

    def adjust_light_distance():
        """Function that monitors the distance between main light and plant. Uses PWM to control motor"""

        global distanceSensor, pwmReverseUp

        while distanceSensor.value() == 1:
            pwmReverseUp.freq(20)
            pwmReverseUp.duty_u16(20000)

    def light_calibration():
        """ Sets light height to correct distance at system start-up """

        global distanceSensor, pwmForwardDown, pwmReverseUp

        pwmReverseUp.freq(400)
        pwmReverseUp.duty_u16(65535)
        sleep(3)
        pwmReverseUp.duty_u16(0)
                
        # lower light until plant is detected
        while distanceSensor.value() == 0:
            pwmForwardDown.freq(400)
            pwmForwardDown.duty_u16(65535)

        pwmForwardDown.duty_u16(0)
            
        pwmForwardDown.duty_u16(0)

    # toggle switch GPIO
    toggle_one   = Pin(2, Pin.IN, Pin.PULL_DOWN)  # Grow phase 1
    toggle_two   = Pin(3, Pin.IN, Pin.PULL_DOWN)  # Grow phase 2
    toggle_three = Pin(4, Pin.IN, Pin.PULL_DOWN)  # Grow phase 3
    toggle_four  = Pin(5, Pin.IN, Pin.PULL_DOWN)  # Grow phase 4
    
    # IR distance sensor
    distanceSensor = Pin(6, Pin.IN, Pin.PULL_DOWN)  # Manual watering
    
    # PWM motors
    pwmForwardDown = PWM(Pin(0, Pin.IN, Pin.PULL_DOWN))
    pwmReverseUp   = PWM(Pin(1, Pin.IN, Pin.PULL_DOWN))

    # timer values
    light_time_on            = 0
    system_timer             = 0
    counter                  = 0
    light_time_off           = 0
    dispensed_water_total    = 0
    pump_two_total           = 0
    pump_three_total         = 0
    water_redundancy_check   = 0
    light_redundancy_check   = 0
    temp_check_value         = 0
    humidity_check_value     = 0
    low_temp_check_value     = 0
    low_humidity_check_value = 0
    error_counter            = 0
    database_values          = []

    # GPIO relay assignments
    relay_1  = Pin(17, Pin.OUT)  # exhaust
    relay_2  = Pin(16, Pin.OUT)  # Main light
    relay_3  = Pin(15, Pin.OUT)  # lateral light
    relay_4  = Pin(14, Pin.OUT)  # Water pump
    relay_5  = Pin(13, Pin.OUT)  # Lateral Lights x3
    relay_6  = Pin(12, Pin.OUT)  # Humidifier
    relay_7  = Pin(11, Pin.OUT)
    relay_8  = Pin(10, Pin.OUT)  # Heat lamps
    relay_9  = Pin(18, Pin.OUT)  # Mini exhaust
    relay_10 = Pin(27, Pin.OUT)
    relay_11 = Pin(26, Pin.OUT)  # Dehumidifier #1
    relay_12 = Pin(22, Pin.OUT)  # Dehumidifier #2
    relay_13 = Pin(21, Pin.OUT)  # Dehumidifier #3
    relay_14 = Pin(20, Pin.OUT)  # Dehumidifier #4
    relay_15 = Pin(19, Pin.OUT)

    # system timers for display and hour counter
    display_timer = Timer(period=20_000, mode=Timer.PERIODIC,
                          callback=display_lcd)  # one minute timer
    timer_one     = Timer(period=3_600_000, mode=Timer.PERIODIC,
                      callback=system_controller)

    # low values
    # set to maximum values for initial running of program to establish low values
    sensor = "sht31"
    temp_f = 212
    temp_c = 100
    hum    = 100

    # ensure all relays are off at the start of program
    relay_1 .value(0)
    relay_2 .value(0)
    relay_3 .value(0)
    relay_4 .value(0)
    relay_5 .value(0)
    relay_6 .value(0)
    relay_7 .value(0)
    relay_8 .value(0)
    relay_9 .value(0)
    relay_10.value(0)
    relay_11.value(0)
    relay_12.value(0)
    relay_13.value(0)
    relay_14.value(0)
    relay_15.value(0)

    # establish system time
    database()

    # Assign values from database() to respected variable
    system_timer           = int(database_values[0])
    water_redundancy_check = int(database_values[2])
    light_redundancy_check = int(database_values[1])
    initial_light_reading  = int(database_values[3])
    relay_2.value(initial_light_reading)
    relay_3.value(initial_light_reading)
    relay_5.value(initial_light_reading)

    # close .txt file
    database()

    # notify user that the program is running
    print("*****Program running*****")

    # loop that constantly runs to monitor state of UART
    while True:

        # solid LED to let user know system is in standby
        system_led = Pin(25, Pin.OUT)
        system_led.value(1)
        while True:  # change to number of plants
            while toggle_one.value() == 1:
                main_body(toggle_one)
            while toggle_two.value() == 1:
                #water_redundancy_check = 0
                main_body(toggle_two)
            while toggle_three.value() == 1:
                #water_redundancy_check = 0
                main_body(toggle_three)
            while toggle_four.value() == 1:
                main_body(toggle_four)
except (TypeError, ValueError, IndexError):
    error_counter += 1
    