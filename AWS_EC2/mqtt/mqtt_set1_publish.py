import paho.mqtt.client as mqtt
import time;
import datetime;

# broker = "127.0.0.1"
broker = "localhost"
port = 1883
ecCommand = [0x0F, 0x03, 0x00, 0x00, 0x00, 0x02, 0xC5, 0x25]
phCommand = [0x0A, 0x03, 0x00, 0x00, 0x00, 0x01, 0x85, 0x71]
waterTempCommand = [0x01, 0x03, 0x00, 0x00, 0x00, 0x01, 0x84, 0x0A]

SET_1_COMMAND = [
    {
    "topic" : "AquaFarm/Set1/Ec/Command",
    "cmd" : ecCommand
    },
    {
    "topic" : "AquaFarm/Set1/Ph/Command",
    "cmd" : phCommand
    },
    {
    "topic" : "AquaFarm/Set1/WaterTemp/Command",
    "cmd" : waterTempCommand
    },
]

SET_2_COMMAND = [
    {
    "topic" : "AquaFarm/Set2/Ec/Command",
    "cmd" : ecCommand
    },
    {
    "topic" : "AquaFarm/Set2/Ph/Command",
    "cmd" : phCommand
    },
    {
    "topic" : "AquaFarm/Set2/WaterTemp/Command",
    "cmd" : waterTempCommand
    },
]


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt.Client(client_id="001")
    client.username_pw_set(username="Publisher1",password="Publisher11234")
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

client = connect_mqtt()
print(datetime.datetime.now())
for i in SET_1_COMMAND:
    #time.sleep(10)
    client.publish(i["topic"], bytes(i["cmd"]))
    print("sent topic: ", i["topic"])
    time.sleep(10)

#for i in SET_2_COMMAND:
#       time.sleep(3)
#       client.publish(i["topic"], bytes(i["cmd"]))
#       print("sent topic: ", i["topic"])
#       #time.sleep(2)

client.disconnect()

