#!/usr/bin/python
import sys
import os
from time import *
import time
from sense_hat import SenseHat
from stick import SenseStick
import threading
import led_display


#bunch of code necessary to make everything work
def data_record(time):
    global min_pressure
    dataOut = ""
    dataOut += str(time) + ", "
    dataOut += str(sense.get_humidity()) + ", " # % relative humidity
    dataOut += str(sense.get_temperature_from_humidity()) + ", " # Temp from Humidity Sensor in C
    #getting the pressure and checking whether it is the lowest pressure (aka highest altitude)
    pressure = sense.get_pressure()
    if min_pressure > pressure:
        min_pressure = pressure
    dataOut += str(pressure) + ", " #pressure is in millibar
    dataOut += str(sense.get_temperature_from_pressure()) + ", " # Temp from Pressure Sensor in C
    dataOut += str(sense.get_compass()) + ", " # Compass - degrees from North
    dataOut += str(sense.get_compass_raw()) + ", "
    dataOut += str(sense.get_gyroscope()) + ", "
    dataOut += str(sense.get_gyroscope_raw()) + ", "
    dataOut += str(sense.get_accelerometer()) + ", "
    dataOut += str(sense.get_accelerometer_raw()) + "\n"
    
    f.write(dataOut)


####################################################################
####################################################################
####################################################################
#initializing the sense hat
sense = SenseHat()
sense.set_imu_config(True, True, True)
stick = SenseStick()


#set some initial parameters and LED display
min_pressure = sense.get_pressure()
start_pressure = min_pressure
start_alt_ft = 0.0
max_alt_ft = 0.0
led_display.init_display()

#opening the output files
filestamp = localtime()
directory = '/home/pi/Desktop/data/'
data_filename = directory + repr(filestamp.tm_year)+'-'+repr(filestamp.tm_mon)+'-'+repr(filestamp.tm_mday)+'__'+repr(filestamp.tm_hour)+'-'+repr(filestamp.tm_min)+'_data.csv'
gps_filename = directory + repr(filestamp.tm_year)+'-'+repr(filestamp.tm_mon)+'-'+repr(filestamp.tm_mday)+'__'+repr(filestamp.tm_hour)+'-'+repr(filestamp.tm_min)+'_gps.csv'
f = open(data_filename, 'w')


####################################################################
####################################################################
####################################################################
# MAIN LOOP
while True:
    timestamp = time.time()
    data_record(timestamp)
    led_display.data_display('data')
    
    #checking if the center joystick has been pushed
    stick_press = stick.wait(timeout=0.01)
    if stick_press:
        event = stick.read()
        if event.state == stick.STATE_PRESS:
            if event.key == stick.KEY_ENTER:
                break

#closing the data files
f.close()

####################################################################
####################################################################
####################################################################
# ALTITUDE REPORTING SCRIPT
while True:
    start_alt_ft = (1 - (start_pressure/1013.25)**0.190284) * 145366.45
    max_alt_ft = (1 - (min_pressure/1013.25)**0.190284) * 145366.45
    sense.show_message("Max Alt: "  + str(round(max_alt_ft-start_alt_ft)) + " ft")
    stick_check2 = stick.wait(timeout=0.1)
    if stick_check2:
        event2 = stick.read()
        if event2.state == stick.STATE_PRESS:
            if event2.key == stick.KEY_ENTER:
                break

####################################################################
####################################################################
####################################################################
# Restart or Shutdown Script -- waiting for user input
R = (60, 150, 177) #reboot color
S = (255, 0, 0) #shutdown color
O = (0, 0, 0) #blank
final_display = [
    O, O, O, O, O, O, O, O,
    O, O, R, O, O, S, O, O,
    O, R, R, O, O, S, S, O,
    R, R, R, O, O, S, S, S,
    R, R, R, O, O, S, S, S,
    O, R, R, O, O, S, S, O,
    O, O, R, O, O, S, O, O,
    O, O, O, O, O, O, O, O,
]

sense.set_pixels(final_display)
while True:
    stick_check3 = stick.wait(timeout=0.01)
    if stick_check3:
        event3 = stick.read()
        if event3.state == stick.STATE_PRESS:
            if event3.key == stick.KEY_LEFT: #restart
                sense.clear()
                os.system("sudo shutdown -r now")
            if event3.key == stick.KEY_RIGHT: #shutdown
                sense.clear()
                os.system("sudo shutdown -h now")
