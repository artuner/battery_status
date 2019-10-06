#!/usr/bin/python3 by SergioPoverony and etc for INA219 battery status 
#in gameboy pi mode gpl2 and etc
from time import sleep
import os
import re
import subprocess
import serial
from subprocess import check_output
from time import sleep
# Config
warning = 0
status = 0
PNGVIEWPATH = "/home/pi/battery_status"
ICONPATH = "/home/pi/battery_status/icons"
CLIPS = 1
REFRESH_RATE = 10
VCC = 4.2
VOLTFULL = 400
VOLT100 = 385
VOLT75 = 375
VOLT50 = 355
VOLT25 = 330
VOLT0 = 322

#position and resolution
fbfile="tvservice -s"
resolution=re.search("(\d{3,}x\d{3,})", subprocess.check_output(fbfile.split()).decode().rstrip()).group().split('x')
dpi=36
width = (int(resolution[0]) - dpi * 2)

def read():
       ser = serial.Serial('/dev/ttyACM0', 9600)
       b = ser.readline()
       return b
       ser.close()
       exit()

def convertVoltage(val):
    global VCC
    voltage = float(val) * (VCC / 255.0)
    return voltage

def changeicon(percent):
    i = 0
    killid = 0
    os.system(PNGVIEWPATH + "/pngview -b 0 -l 30001" + " -x " + str(width) + " -y 5 " + ICONPATH + "/battery" + percent + ".png &")
    out = check_output("ps aux | grep pngview | awk '{ print $2 }'",shell=True)
    nums = out.split('\n')
    for num in nums:
        i += 1
        if i == 1:
            killid = num
            os.system("sudo kill " + killid)

os.system(PNGVIEWPATH + "/pngview -b 0 -l 299999" + " -x " + str(width) + " -y 5 " + ICONPATH + "/blank.png &")

while True:
        val1 = read()
        val1 = float(val1.strip())
        #print val1
        val2 = read()
        val2 = float(val2.strip())
        #print val2
        val3 = read()
        val3 = float(val3.strip())
        #print val3
        val4 = read()
        val4 = float(val4.strip())
        #print val4
        val5 = read()
        val5 = float(val5.strip())
        #print val5
        val6 = read()
        val6 = float(val6.strip())
        #print val6
        val7 = read()
        val7 = float(val7.strip())
        #print val7
        val8 = read()
        val8 = float(val8.strip())
        #print val8
        val9 = read()
        val9 = float(val9.strip())
        #print val9
        ret = (float(val1+val2+val3+val4+val5+val6+val7+val8+val9)/9.0)
	print ret
	if ret < VOLT0:
		if status != 0:
			#print
			changeicon("0")
			if CLIPS == 1:
				os.system("/usr/bin/aplay " + ICONPATH + "/LowBattery.wav")
				voltcheck = (read())
				if voltcheck <= VOLT0:
					os.system(PNGVIEWPATH + "/pngview -b 0 -l 299999" + " -x "+ str(int(resolution[0])/2-128)+ " -y " + str(int(resolution[1])/2-128) + " " + ICONPATH + "/alert-outline-red.png &")
					os.system("sleep 60 && sudo poweroff &")
					warning = 1
				else:
					warning = 0
		status = 0
	elif ret < VOLT25:
		if status != 25:
			changeicon("25")
			if warning != 1:
				if CLIPS == 1:
					os.system("/usr/bin/aplay " + ICONPATH + "/LowBattery.wav")
				warning = 1
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
