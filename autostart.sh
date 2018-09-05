internet=true
SECONDS=$(date +"%s")
while ! ifconfig | grep "172\.20\.94\." > /dev/null;
do
	echo "Wifi still not connected..."
	if [ $(($(date +"%s")-$SECONDS)) -gt 5 ]; then
		internet=false
		echo "Internet connection timed out."
		break
	fi
done
if $internet ;
then
	git -C /home/pi/kiosk/client pull
fi
python /home/pi/kiosk/client/client.py &
