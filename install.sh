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
if ! grep -Fxq "python /home/pi/battery_status/battery.py &" /etc/rc.local
then
sed -i "s/^exit 0/python \/home\/pi\/battery_status\/battery.py \&\\nexit 0/g" /etc/rc.local >/dev/null
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
#if grep -q 'dtparam=i2c1=on' /boot/config.txt; then
#  echo 'Seems i2c1 parameter already set, skip this step.'
#else
#  echo 'dtparam=i2c1=on' >> /boot/config.txt
#fi
#if grep -q 'dtparam=i2c_arm=on' /boot/config.txt; then
#  echo 'Seems i2c_arm parameter already set, skip this step.'
#else
#  echo 'dtparam=i2c_arm=on' >> /boot/config.txt
#fi

#overwrite cmdline, for cleaner startup
#breaks raspbian stretch, disabled for now
#cp -f /boot/battery/configs/cmdline.txt /boot/cmdline.txt

#remove DHCP wait, for faster bootup
#rm -f /etc/systemd/system/dhcpcd.service.d/wait.conf

#add custom startup image
#cp -f /boot/battery/theme/battery.png /home/pi/RetroPie/splashscreens/battery.png
#cp -f /boot/battery/theme/splashscreen.list /etc/splashscreen.list

#modify theme
#also, figure out how to change theme so the scrolling is instant instead of fade
#also, figure out how to set "power save mode" to Enhanced
#cp -f /boot/battery/theme/carbon.xml /etc/emulationstation/themes/carbon/carbon.xml
#cp -f /boot/battery/theme/background.png /etc/emulationstation/themes/carbon/art/background.png

#add WiFi options tand othermod menu
#change this so it asks whether you have a Zero W (or better yet, detects whether it's a Zero W), and doesn't WiFi files if the answer is no
#cp -p -r -f  /boot/battery/theme/scripts /home/pi/RetroPie/othermod
#cp -f /boot/battery/theme/es_systems.cfg /etc/emulationstation/es_systems.cfg
#cp -p -r -f  /boot/battery/theme/system /etc/emulationstation/themes/carbon/othermod

read -rsp $'Press any key to reboot...\n' -n1 key

chmod 755 /home/pi/battery_status/Pngview/pngview

reboot

