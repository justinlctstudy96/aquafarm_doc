import pygame, time, datetime;
import pygame.camera;
import subprocess, requests, json
import paho.mqtt.client as mqtt

'''mqtt connection'''
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("aqua_farm/sensors")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

print("Begin at ", datetime.datetime.now());

try:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username="Muselab",password="Muselab1234")
    # client.connect("218.253.145.198", 18088, 60)
    client.connect("13.228.53.179", 1883, 60)
    print("mqtt connected");
except Exception as ex:
    print("MQTT client connection error " + str(ex))
    # client.connect("218.253.145.198", 18088, 60)
    client.connect("13.228.53.179", 1883, 60)
    pass;
    #exit()

pygame.camera.init();
availableCamera = pygame.camera.list_cameras();

# camera connection
if ( "/dev/video0" in availableCamera ):
    cam0 = pygame.camera.Camera("/dev/video0",(640,480))
    print("cam0 connected");
else:
    client.publish("AquaFarm/HongKong/Image/Error", json.dumps({"CAM0":"unable to locate"}))
    print("cam0 unable to locate");

if ( "/dev/video2" in availableCamera ):
    cam1 = pygame.camera.Camera("/dev/video2",(640,480))
    print("cam1 connected");
else:
    client.publish("AquaFarm/HongKong/Image/Error", json.dumps({"CAM1":"unable to locate"}))
    print("cam1 unable to connect");
    
if ('cam0' not in locals() and 'cam1' not in locals()):
    print("No camera is connected; exit");
    exit();
    
# image saving
if 'cam0' in locals() :
    cam0.start()
    img0 = cam0.get_image()
    pygame.image.save(img0,"camera0.jpg")
    #time.sleep(2)
    cam0.stop();
    print("cam0 image saved");
else:
    client.publish("AquaFarm/HongKong/Image/Error", json.dumps({"CAM0":"cannot save image"}))
    print("cam0 cannot save image");

if 'cam1' in locals():
    cam1.start()
    img1 = cam1.get_image()
    pygame.image.save(img1,"camera1.jpg")
    #time.sleep(2)
    cam1.stop();
    print("cam1 image saved");
else:
    client.publish("AquaFarm/HongKong/Image/Error", json.dumps({"CAM1":"cannot save image"}))
    print("cam1 cannot save image");

    
#image posting
#urlForCam0 = 'http://218.253.145.198:18087/upload/camera0'
#urlForCam1 = 'http://218.253.145.198:18087/upload/camera1'
urlForCam0 = 'http://13.228.53.179:8080/upload/camera0'
urlForCam1 = 'http://13.228.53.179:8080/upload/camera1'
print("before requesting")

files0 = {'camera0': open("camera0.jpg", 'rb')}
try:
    response0 = requests.post(urlForCam0, files=files0)
    print("cam0 image posted");
except requests.exceptions:
    client.publish("AquaFarm/HongKong/Image/Error", json.dumps({"CAM0":"cannot POST image due to {r}".format(r = response0.raise_for_status())}))


files1 = {'camera1': open("camera1.jpg", 'rb')}
try:
    response1 = requests.post(urlForCam1, files=files1)
    print("cam1 image posted");
except requests.exceptions:
    client.publish("AquaFarm/HongKong/Image/Error", json.dumps({"CAM1":"cannot POST image due to {r}".format(r = response1.raise_for_status())}))

exit();
