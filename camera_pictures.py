#!/usr/bin/python
import sys
import os
from time import *
from picamera import PiCamera
import threading
from stick import SenseStick
import led_display

#initializing the camera
camera = PiCamera()
#camera.rotation = 180 #use this if the camera rotation is not correct
camera.resolution = (3280, 2464) #this can be changed

#starting the Sense Stick
joystick = SenseStick()

#opening the output files
filestamp = localtime()
delay = 1 #use this number to set the delay between camera captures in seconds
pic_number = 1 #this is the starting number for taking pictures
pic_dir = "/home/pi/Desktop/Pictures" + repr(filestamp.tm_year)+'-'+repr(filestamp.tm_mon)+'-'+repr(filestamp.tm_mday)+'__'+repr(filestamp.tm_hour)+'-'+repr(filestamp.tm_min)
system_command = "mkdir " + pic_dir
os.system(system_command)
camera_check = True

## This is the main picture taking loop
while camera_check:
    camera.capture(pic_dir + '/image%s.jpg' % pic_number)
    pic_number += 1

    led_display.data_display('camera')

    joystick_press = joystick.wait(timeout=delay)
    if joystick_press:
        event = joystick.read()
        if event.state == joystick.STATE_PRESS:
            if event.key == joystick.KEY_ENTER:
                camera_check = False

