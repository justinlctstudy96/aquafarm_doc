# AquaFarm MQTT & HTTP Structure (eg. Set1)
## Amazon EC2 Servers
    Python Scripts
        MQTT broker: 
            localhost:1883
        /home/mqtt/mqtt_set1_subscribe.py
            subscribe to MQTT topic:
                “AquaFarm/Set1”
            publish to MQTT topics:
                “AquaFarm/Set1/Ec/Value”
                “AquaFarm/Set1/Ph/Value”
                “AquaFarm/Set1/WaterTemp/Value”
        /home/mqtt/mqtt_set1_publish.py
            publish to MQTT topics:
                “AquaFarm/Set1/Ec/Command”
                “AquaFarm/Set1/Ph/Command”
                “AquaFarm/Set1/WaterTemp/Command”
    InfluxDB with Elegraf
        subscribe topic:
            “AquaFarm/+/+/Value”

## USR-DR404 (RS485 to WiFi and Ethernet Converter)
    MQTT broker:
        13.228.53.179:1883
    subscribe to MQTT topics:
        “AquaFarm/Set1/Ec/Command”
        “AquaFarm/Set1/Ph/Command”
        “AquaFarm/Set1/WaterTemp/Command”
    publish to MQTT topic:
        “AquaFarm/Set1

## Raspberry Pi
    Python Scripts
        MQTT broker:
            13.228.53.179:1883
        ~/Desktop/weather_station.py
            subscribe to MQTT topic:
                “aqua_farm/sensors”
            publish to MQTT topic: 
                “AquaFarm/Set1/Weather/Value”
        ~/Desktop/routineImageTaking.py
            subscribe to MQTT topic:
                “aqua_farm/sensors”
            HTTP POST API:
                “http://13.228.53.179:8080/upload/camera0”
                “http://13.228.53.179:8080/upload/camera1” 


# Amazon EC2 Configuration
AWS account
    username: casey.lai@muselab.cc
    pw: Aws2022!
EC2
    region: Singapore
    name: AquaFarm
    public IP: 13.228.53.179
Terminal ssh connection
Hostname: 13.228.53.179
User: ubuntu
Identiy PEM file:
-----BEGIN RSA PRIVATE KEY-----

-----END RSA PRIVATE KEY-----

Cronjob - MQTT subscription and publishing
sudo crontab -e
@reboot python3 /home/mqtt/mqtt_set1_subscribe.py >> /home/mqtt/set1_sub.log 2>&1
* * * * * ( sleep 10 ; python3 /home/mqtt/mqtt_set1_publish.py >> /home/mqtt/set1_pub.log 2>&1 )
# * * * * * ( sleep 30 ; python3 /home/mqtt/mqtt_set2_publish.py >> /home/mqtt/set2_pub.log 2>&1 )
/home/mqtt/mqtt_set1_subscribe.py
subscribe to MQTT topic: “AquaFarm/Set1”
(data from USR-DR404 - RS485 to WiFI) 
on each MQTT message
=>identify data from Ec/Ph/WaterTemp sensor and publish to topic:
“AquaFarm/Set1/Ec/Value” or
“AquaFarm/Set1/Ph/Value” or
“AquaFarm/Set1/WaterTemp/Value”
/home/mqtt/mqtt_set1_publish.py
publish commands to Ec & Ph & WaterTemp sensors topics:
“AquaFarm/Set1/Ec/Command” &
“AquaFarm/Set1/Ph/Command” &
“AquaFarm/Set1/WaterTemp/Command” 
Telegraf of influxdb (put mqtt data to influxdb)
sudo nano /etc/telegraf/telegraf.conf
[[inputs.mqtt_consumer]] (^w => mqtt_consumer)
servers = [“tcp://127.0.0.1:1883”]
topic = [
  “telegraf/host01/cpu”,
  “telegraf/+/mem”,
  “sensors/#”,
  “AquaFarm/+/+/Value”,
]
qos = 1
connection_timeout = “30s”
username = “InfluxUser”
password = “InfluxUser1234”
data_format = “json”
[[outputs.influxdb_v2]] (^w => influxdb_v2)
urls = [“http://127.0.0.1:8086”]
token = “redhgarj_VmTstQMzStHVd8Flq7xPHZIJcYa6MslwhD9OClMIssrQBCt_Bi1h7FaKLn8ZMMOSQMxgvgXKGcmTw==”
organization = “AquaGreen”
bucket = “AquaFarm”
Camera Node.js server
cd /home/camera_server
node index.js

# Raspberry Pi Configuration
sudo crontab -e
@reboot python3 /home/mqtt/mqtt_set1_subscribe.py >> /home/mqtt/set1_sub.log 2>&1
@midnight sudo /sbin/shutdown -r now
* * * * * python3 /home/pi/Desktop/routineImageTaking.py >> /home/pi/Desktop/imageTake.log 2>&1
@reboot python3 /home/pi/Desktop/weather_station.py >> /home/pi/Desktop/weatherStation.log 2>&1
/home/pi/Desktop/weather_station.py
on serial reading
=> publish to MQTT topic: “AquaFarm/Set1/Weather/Value”
/home/pi/Desktop/routineImageTaking.py
camera connection
image saving
image HTTP posting
POST to ‘http://13.228.53.179:8080/upload/camera0’
POST to ‘http://13.228.53.179:8080/upload/camera1’ 


USR-DR404 (RS485 to WiFi) Configuration
Connect to WiFi USR-DR404_9098
go to http://10.10.100.254/home.html
login:
user: admin
password: admin
APSTA setting

MQTT publishing setting

MQTT subscription setting


