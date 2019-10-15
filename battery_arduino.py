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
import signal

#Config
warning = 0
status = 0
debug = 1
PNGVIEWPATH = "/home/pi/battery_status"
ICONPATH = "/home/pi/battery_status/icons"
CLIPS = 1
REFRESH_RATE = 3
VCC = 4.2
VOLTFULL = 410
VOLT100 = 376
VOLT75 = 368
VOLT50 = 352
VOLT25 = 338
VOLT0 =  319


#position and resolution
fbfile="tvservice -s"
resolution=re.search("(\d{3,}x\d{3,})", subprocess.check_output(fbfile.split()).decode().rstrip()).group().split('x')
dpi=36
width = (int(resolution[0]) - dpi * 2)

def readSerial():
    ser.write('1')
    time.sleep(.3)
    x = (ser.readline())
    return x

def read():
    ser = serial.Serial('/dev/ttyACM0', 9600)
    b = ser.readline()
    numV = float(b.strip())
    ser.close()
    return numV	
    exit()

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


# Check Serial Port Availability

while port == 0:
    for x in range(0, 3):
        try:
            ser = serial.Serial('/dev/ttyACM' + str(x), 9600)
        except serial.SerialException:
            if debug == 1:
                print('Serial Port ACM' + str(x) + ' Not Found')
            time.sleep(1)
        else:
            port = 1
            break
		
		
while True:
	print readSerial
	val1 = read()
	sleep(0.16)
	val2 = read()
	sleep(0.16)
	val3 = read()
	sleep(0.16)
	val4 = read()
	sleep(0.16)
	val5 = read()
	sleep(0.16)
	val6 = read()
	sleep(0.16)
	val7 = read()
	sleep(0.16)
	val8 = read()
	sleep(0.16)
	val9 = read()
	ret = (round(val1+val2+val3+val4+val5+val6+val7+val8+val9)/9.0) + 10
	print ret
	print warning
	if ret < VOLT0:
		if status != 0:
			#print
			changeicon("0")
			if CLIPS == 1:
				voltcheck = (read())
				if voltcheck <= VOLT0:
					if warning == 0:
						os.system("/usr/bin/aplay " + ICONPATH + "/LowBattery.wav")
						warning = 1
					elif warning == 1:
						os.system("/usr/bin/aplay " + ICONPATH + "/LowBattery.wav")
						warning = 2
					elif warning == 2:
						os.system("/usr/bin/aplay " + ICONPATH + "/LowBattery.wav")
						os.system(PNGVIEWPATH + "/pngview -b 0 -l 299999" + " -x "+ str(int(resolution[0])/2-128)+ " -y " + str(int(resolution[1])/2-128) + " " + ICONPATH + "/alert-outline-red.png &")
						os.system("sleep 60 && sudo poweroff &")
		status = 0
	elif ret < VOLT25:
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
