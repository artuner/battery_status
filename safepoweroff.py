import RPi.GPIO as GPIO
from time import sleep
import os

GPIO.setmode(GPIO.BCM)
#Set gpio default 4
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(4)
    if input_state == False:
        os.system("sudo shutdown -h now")
    sleep(0.4)