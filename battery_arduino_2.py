#!/usr/bin/python
# based on the following:
# https://github.com/joachimvenaas/gbzbatterymonitor
# by SergioPoverony and etc
# for Arduino 5V battery status in gameboy pi mode
# GPL2 and etc
from time import sleep
import os
import re
import subprocess
from subprocess import check_output
import serial

#Config
warning = 0
status = 0
PNGVIEWPATH = "/home/pi/battery_status"
ICONPATH = "/home/pi/battery_status/icons"
CLIPS = 1
REFRESH_RATE = 1
VCC = 4.2
VOLTFULL = 410
VOLT100 = 400
VOLT75 = 380
VOLT50 = 360
VOLT25 = 340
VOLT0 =  322

#position and resolution
fbfile="tvservice -s"
resolution=re.search("(\d{3,}x\d{3,})", subprocess.check_output(fbfile.split()).decode().rstrip()).group().split('x')
dpi=36
width = (int(resolution[0]) - dpi * 2)

def read():
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    values = []
    for n in range(1, 8):
     try:
      values.append(float(ser.readline()))
     except:
      a = 2419.69
      pass
    ser.close()
    a = float(sum(values)) / max(len(values), 1)
    a = int(a)
    if 200 < a:
     return round(a)

def changeicon(percent):
    i = 0
    killid = 0
    os.system(PNGVIEWPATH + "/pngview -b 0 -l 30001" + " -x " + str(width) + " -y 5 " + ICONPATH + "/battery" + percent + ".png &")
    out = check_output("ps aux | grep pngview | awk '{ print $2 }'", shell=True)
    nums = out.split('\n')
    for num in nums:
        i += 1
        if i == 1:
            killid = num
            os.system("sudo kill " + killid)

os.system(PNGVIEWPATH + "/pngview -b 0 -l 299999" + " -x " + str(width) + " -y 5 " + ICONPATH + "/blank.png &")

while True:
	ret = read()
	print ret
	if ret < VOLT0:
		#if status != 0:
		#REFRESH_RATE = 100
		changeicon("0")
		#if CLIPS == 1:
		if warning == 0:
			print ret
			warning = 1
			os.system("/usr/bin/aplay " + ICONPATH + "/LowBattery.wav")
		elif warning == 1:
			print ret
			warning = 2
			os.system("/usr/bin/aplay " + ICONPATH + "/LowBattery.wav")
		elif warning == 2:
			print ret
			os.system("/usr/bin/aplay " + ICONPATH + "/LowBattery.wav")
			os.system(PNGVIEWPATH + "/pngview -b 0 -l 299999" + " -x "+ str(int(resolution[0])/2-128)+ " -y " + str(int(resolution[1])/2-128) + " " + ICONPATH + "/alert-outline-red.png &")
			os.system("sleep 60 && sudo poweroff &")
		status = 0
	elif ret < VOLT25:
		REFRESH_RATE = 300
		if status != 25:
			changeicon("25")
			warning = 0
		status = 25
	elif ret < VOLT50:
		if status != 50:
			changeicon("50")
		status = 50
	elif ret < VOLT75:
		if status != 75:
			changeicon("75")
		status = 75
	elif ret < VOLT100:
		if status != 100:
			changeicon("100")
		status = 100
	else:
		if status != -1:
			changeicon("FULL")
		status = -1
	sleep(REFRESH_RATE)
