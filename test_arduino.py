#!/usr/bin/python3
#by SergioPoverony and etc
#for Arduino 5V battery status in gameboy pi mode
#GPL2 and etc
from time import sleep
import os
import re
import subprocess
from subprocess import check_output
import serial

REFRESH_RATE = 1

def read():
    ser = serial.Serial('/dev/ttyACM0', 9600)
    values = []
    for i in range(1, 15):
     values.append(float(ser.readline().strip(",\n\r")))
    ser.close()
    return float(sum(values)) / max(len(values), 1)
    exit()

while True:
	ret = round(read() + 10)
	print ret
	sleep(REFRESH_RATE)

