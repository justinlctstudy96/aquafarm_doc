import paho.mqtt.client as mqtt
import json
# import time, datatime
import time
from datetime import datetime

broker = '127.0.0.1'
port = 1883

SET_1_TOPIC = "AquaFarm/Set1"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt.Client(client_id="Set1Subscriber")
    client.username_pw_set(username="Subscriber1",password="Subscriber11234")
    client.on_connect = on_connect
    client.connect(broker, port)
    # client.enable_logger(logger=MQTT_LOG_DEBUG)
    return client

def subscribe(client: mqtt):
    def on_message(client, userdata, msg):
        print("===================================================")
        print(datetime.now())
        print(msg.topic, ": ", msg.payload)
        hexString = ""
        valueObject = {}
        topic = ""
        for i in range(len(msg.payload)):
            variable = hex(msg.payload[i])[2:]
            if ( len(variable) == 1 ):
                hexString += "0" + variable
            else:
                hexString += hex(msg.payload[i])[2:]
        if(hexString[:2] == "0f"):
            EChexString = hexString
            EC = round(int(EChexString[6:14], 16) * 0.1/ 10, 2)
            topic = msg.topic + "/EC/Value"
            valueObject["EC"] = EC
        if(hexString[:2] == "0a"):
            PHhexString=PHhexString = hexString
            PH = round(int(PHhexString[6:10], 16) * 0.1 / 10, 2)
            topic = msg.topic + "/Ph/Value"
            valueObject["PH"] = PH
        if(hexString[:2] == "01"):
            WaterTemphexString = hexString
            WaterTemp = round(int(WaterTemphexString[6:10], 16) / 100 - 50, 2)
            topic = msg.topic + "/WaterTemp/Value"
            valueObject["WaterTemp"] = WaterTemp
        if (topic and valueObject):
            client.publish(topic, json.dumps(valueObject))
            print(topic, valueObject)
    MQTT_TOPIC = [(SET_1_TOPIC, 1)]
    client.subscribe(MQTT_TOPIC)
    client.on_message = on_message

try:
    time.sleep(20)
    print(datetime.now())
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
except Exception as ex:
    print("exception")
    print(ex)
    pass
