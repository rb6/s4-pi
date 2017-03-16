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

#initializing the Sense Stick
joystick = SenseStick()

## Resolution, Aspect ratio, Framerate table
# (1920, 1080), 16:9,   0.1-30 fps
# (3280, 2464), 4:3,    0.1-15 fps
# (1640, 1232), 4:3,    0.1-40 fps
# (1640, 922),  16:9,   0.1-40 fps
# (1280, 720),  16:9,   40-90 fps
# (640, 480),   4:3,    40-90 fps

#setting the resolution and framerate
camera.resolution = (640, 480)
camera.framerate = 90

#initializing additional variables
filestamp = localtime()
vid_dir = '/home/pi/Desktop/Videos/'
if not os.path.isdir(vid_dir):
    os.makedirs(vid_dir)
vid_name = 'Video_'+repr(filestamp.tm_year)+'-'+repr(filestamp.tm_mon)+'-'+repr(filestamp.tm_mday)+'__'+repr(filestamp.tm_hour)+'-'+repr(filestamp.tm_min)+'.h264'
camera_check = True
old_time = time()

## This is the main video loop -- will record video until told to turn off
camera.start_recording(vid_dir+vid_name) #start recording the video
while camera_check:
    cur_time = time()
    if ((cur_time-old_time) >= 1.0):
        led_display.data_display('camera')

    joystick_press = joystick.wait(timeout = 1)
    if joystick_press:
        event = joystick.read()
        if event.state == joystick.STATE_PRESS:
            if event.key == joystick.KEY_ENTER:
                camera_check = False
camera.stop_recording() #stop recording the video

    
