File structure that these scripts expect.

All scripts reside in the /home/pi/Desktop/Scripts folder
By in large they should not be dependent on where they are
because the paths to other folders are hard-coded, not
from a relative path.

stick.py and led_display_v2.py are helper scripts. They
need to be at the same level as s4data_v3.py and the two
camera*.py scripts.

s4data_v3.py is the main data aquisition script. It
expects a data folder on the desktop:
/home/pi/Desktop/data

Realistically, the script could point to the desktop or
anywhere else as long as the permissions allow it to
write to the location.

camera_video.py expects to record the video to a folder on
the destop:
/home/pi/Desktop/Videos

camera_pictures.py will create a folder on the desktop
each time it executes to save the pictures to.
