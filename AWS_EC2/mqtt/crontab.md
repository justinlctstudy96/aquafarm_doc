sudo crontab -e


@reboot python3 /home/mqtt/mqtt_set1_subscribe.py >> /home/mqtt/set1_sub.log 2>&1

* * * * * ( sleep 10 ; python3 /home/mqtt/mqtt_set1_publish.py >> /home/mqtt/set1_pub.log 2>&1 )

# * * * * * ( sleep 30 ; python3 /home/mqtt/mqtt_set2_publish.py >> /home/mqtt/set2_pub.log 2>&1 )