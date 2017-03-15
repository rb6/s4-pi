#!/usr/bin/python
from sense_hat import SenseHat

#starting the Sense Stick
sense_display = SenseHat()


#initializing and creating the function for the LED display that will be updated during data record
#the display will be split into 2 sections (top 4 rows and bottom 4 rows), the top will show data
#being recorded for the sensors and the bottom will show data being recorded for the GPS

#thinking the colors will be the following:
#Data Record: Background=Purple, Foreground=Yellow
#Camera Record: Background=Blue, Foreground=Orange
P = (128, 0, 128)
Y = (255, 255, 0)
B = (0, 0, 255)
O = (255, 163, 0)
display_counter_data = 0
display_counter_camera = 48
display_check_data = 0 #0 is for going up, 1 is going down
display_check_camera = 0 #0 is for going up, 1 is going down

led_matrix_data = [
    P, P, P, P, P, P, P, P,
    P, P, P, P, P, P, P, P,
    P, P, P, P, P, P, P, P,
    P, P, P, P, P, P, P, P,
    P, P, P, P, P, P, P, P,
    P, P, P, P, P, P, P, P
]

led_matrix_camera = [
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B
]

#setting up the display for Data record
#setting up the display for the Camera and Data record
# source = 'data' for Data
# source = 'camera' for GPS
def data_display(source):
    global display_counter_data
    global display_counter_camera
    global display_check_data
    global display_check_camera
    global led_matrix_data
    global led_matrix_camera
    
    led_matrix2 = sense_display.get_pixels()
    
    if source == 'data':
        if display_check_data == 0:
            led_matrix2[display_counter_data] = Y
        else:
            led_matrix2[display_counter_data] = P
        display_counter_data += 1
        
    else:
        if display_check_camera == 0:
            led_matrix2[display_counter_camera] = O
        else:
            led_matrix2[display_counter_camera] = B
        display_counter_camera += 1
        
    if display_counter_data == 48:
        if display_check_data == 0:
            display_check_data = 1
        else:
            display_check_data = 0
        display_counter_data = 0
    
    if display_counter_camera == 64:
        if display_check_camera == 0:
            display_check_camera = 1
        else:
            display_check_camera = 0
        display_counter_camera = 48

    sense_display.set_pixels(led_matrix2)

#initializing the display
def init_display():
    global led_matrix_data
    global led_matrix_camera
    output = led_matrix_data + led_matrix_camera
    sense_display.set_pixels(output)
