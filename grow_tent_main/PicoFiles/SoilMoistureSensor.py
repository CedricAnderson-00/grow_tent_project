from machine import ADC, Pin
import utime

def soil_sensor_one():
    """Function that reads soil sensor one and returns a value as a percentage.
       Each soil sensor value is specific to itself"""
    
    soil1 = ADC(Pin(28))    
    min_moisture = 30200
    max_moisture = 56285
    moisture = (max_moisture - soil1.read_u16()) * 100 / (max_moisture - min_moisture)
    
    return moisture


def soil_sensor_two():
    """Function that reads soil sensor one and returns a value as a percentage.
       Each soil sensor value is specific to itself"""
    
    soil2 = ADC(Pin(27))    
    min_moisture = 32400
    max_moisture = 56893
    moisture = (max_moisture - soil2.read_u16()) * 100 / (max_moisture - min_moisture)
    
    return moisture


def soil_sensor_three():
    """Function that reads soil sensor one and returns a value as a percentage.
       Each soil sensor value is specific to itself"""
    
    soil3 = ADC(Pin(26))    
    min_moisture = 32425
    max_moisture = 56893
    moisture = (max_moisture - soil3.read_u16()) * 100 / (max_moisture - min_moisture)
    
    return moisture
