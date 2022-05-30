sudo crontab -e

@midnight sudo /sbin/shutdown -r now
* * * * * python3 /home/pi/Desktop/routineImageTaking.py >> /home/pi/Desktop/imageTake.log 2>&1
@reboot python3 /home/pi/Desktop/weather_station.py >> /home/pi/Desktop/weatherStation.log 2>&1