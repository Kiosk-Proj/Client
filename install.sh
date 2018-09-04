#!/bin/sh

#install Adafruit
echo Installing Adafruit Libraries...
cd /tmp
git clone https://github.com/adafruit/Adafruit_Python_CharLCD
cd Adafruit_Python_CharLCD
sudo python setup.py install
cd /
echo Installation Complete... Deleting temporary library sources...
sudo rm -rf /tmp/Adafruit_Python_CharLCD

#Make directories if they don't already exist
echo Creating file structure...
cd ~
if [ ! -d "kiosk" ]
then
	mkdir kiosk
fi
cd kiosk
if [ ! -d "client" ]
then
	mkdir client
fi

echo Cloning sources...
git clone https://github.com/Kiosk-Proj/Client client

curl http://96.225.21.203:8080/get > /home/pi/kiosk/client/ini.txt
cd client

#Add to startup script
echo Setting startup script...
sudo sed -i $(wc -l /etc/network/interfaces | cut -f1 -d' ')'icurl http://96.225.21.203:8080/get?'$1' > /home/pi/kiosk/client/ini.txt && python /home/pi/kiosk/client/client.py &' /etc/rc.local
echo Installation complete!
