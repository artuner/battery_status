#!/bin/bash
# https://www.othermod.com
if [ $(id -u) -ne 0 ]; then
	echo "Installer must be run as root."
	echo "Try 'sudo bash $0'"
	exit 1
fi

echo "Configuring Battery to start at boot..."

#boot script should have the necessary lines(Battery, poweroff, backlight, buttons), then new ones should be added after a y/n question(joystick)
# Insert battery script into rc.local before final 'exit 0'
if ! grep -Fxq "python /home/pi/battery_status/battery_ina219.py &" /etc/rc.local
then
sed -i "s/^exit 0/python \/home\/pi\/battery_status\/battery_ina219.py \&\\nexit 0/g" /etc/rc.local >/dev/null
fi

# enable I2C on Raspberry Pi
echo '>>> Enable I2C'
if grep -q 'i2c-bcm2708' /etc/modules; then
  echo 'Seems i2c-bcm2708 module already exists, skip this step.'
else
  echo 'i2c-bcm2708' >> /etc/modules
fi
if grep -q 'i2c-dev' /etc/modules; then
  echo 'Seems i2c-dev module already exists, skip this step.'
else
  echo 'i2c-dev' >> /etc/modules
fi

chmod 0775 /home/pi/battery_status/pngview
read -rsp $'Press any key to reboot...\n' -n1 key
reboot

