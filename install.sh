#!/bin/bash

#install Adafruit
cd /tmp
git clone https://github.com/adafruit/Adafruit_Python_CharLCD
cd Adafruit_Python_CharLCD
sudo python setup.py install
cd /
sudo rm -rf /tmp/Adafruit_Python_CharLCD

#Make directories if they don't already exist
cd ~
if [ ! -d "kiosk" ] then
	mkdir kiosk
fi
cd kiosk
if [ ! -d "client" ] then
	mkdir client
fi

git clone https://github.com/Kiosk-Proj/Client client

cd client

#Add to startup script
sudo sed -i $(wc -l /etc/network/interfaces | cut -f1 -d' ')'ipython /home/pi/kiosk/client/client.py &' /etc/rc.local