
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

#Config
warning = 0
status = -1
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

def read():
    ser = serial.Serial('/dev/ttyACM0', 9600)
    values = []
    for i in range(0, 15):
     values.append(float(ser.readline()))
    ser.close()
    return float(sum(values)) / max(len(values), 1)
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


while True:
	print read()
	ret = read()
	print warning
	if ret < VOLT0:
		if status != 0:
			print "status"
			changeicon("0")
			if CLIPS == 1:
				if warning == 0:
					print "warning 1"
					warning = 1
					os.system("/usr/bin/aplay " + ICONPATH + "/LowBattery.wav")
				elif warning == 1:
					print "warning 2"
					warning = 2
					os.system("/usr/bin/aplay " + ICONPATH + "/LowBattery.wav")
				elif warning == 2:
					print "Power Off"
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
