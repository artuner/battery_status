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
#if ! grep -Fxq "python /home/pi/battery_status/battery_arduino.py &" /etc/rc.local
#then
#sed -i "s/^exit 0/python \/home\/pi\/battery_status\/battery_arduino.py \&\\nexit 0/g" /etc/rc.local >/dev/null
#fi
chmod 0775 /home/pi/battery_status/pngview
sudo cp /home/pi/battery_status/battery.service /etc/systemd/system/battery.service
sudo chmod +x /etc/systemd/system/battery.service
read -rsp $'Press any key to reboot...\n' -n1 key
reboot



