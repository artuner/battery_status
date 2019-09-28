#!/usr/bin/python3
#by SergioPoverony and etc
#for INA219 battery status in gameboy pi mode
#gpl2 and etc
from smbus import SMBus
from time import sleep
import os
import re
import subprocess

from subprocess import check_output

bus = SMBus(1)
addr = 0x13

from ina219 import INA219, DeviceRangeError

from time import sleep

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 2.0
ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
ina.configure(ina.RANGE_16V)

addr=ina.voltage()


# Config
warning = 0
status = 0
PNGVIEWPATH = "/home/pi/battery_status"
ICONPATH = "/home/pi/battery_status/icons"
CLIPS = 1
REFRESH_RATE = 2
VCC = 4.2
VOLTFULL = 400
VOLT100 = 380
VOLT75 = 365
VOLT50 = 345
VOLT25 = 330
VOLT0 =  300


#position and resolution
fbfile="tvservice -s"
resolution=re.search("(\d{3,}x\d{3,})", subprocess.check_output(fbfile.split()).decode().rstrip()).group().split('x')
dpi=36
width = (int(resolution[0]) - dpi * 2)

def read():
        return int(ina.voltage()*100)

def convertVoltage(val):
    global VCC
    voltage = float(val) * (VCC / 255.0)
    return voltage

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
	val1 = read()
	sleep(3)
	val2 = read()
	sleep(3)
	val3 = read()
	ret = (float(val1+val2+val3)/3.0)
	#print ret
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
