from smbus import SMBus
from time import sleep
import os
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
REFRESH_RATE = 10
VCC = 4.2
VOLTFULL = 380
VOLT100 = 375
VOLT75 = 355
VOLT50 = 330
VOLT25 = 310
VOLT0 =  270
width = 560

def read():
        return int(ina.voltage()*100)

def convertVoltage(val):
    global VCC
    voltage = float(val) * (VCC / 255.0)
    return voltage


while True:
	val1 = read()
	sleep(2)
	val2 = read()
	sleep(2)
	val3 = read()
	ret = (float(val1+val2+val3)/3.0)
	print ret
	sleep(REFRESH_RATE)
