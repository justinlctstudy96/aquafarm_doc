import serial, time, json, sys, datetime, random
import paho.mqtt.client as mqtt

ser = serial.Serial()
ser.port = "/dev/serial/by-id/usb-1a86_USB2.0-Ser_-if00-port0"
ser.baudrate = 9600
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.timeout = 0.5
ser.writeTimeout = 0.5
ser.xonxoff = False
ser.rtscts = False
ser.dsrdtr = False

'''mqtt connection'''
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("aqua_farm/sensors")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

'''station decode'''
def wind_direction(raw_hex_data):
    WIND_DIRECTION_hex_string = raw_hex_data[4:7]
    WIND_DIRECTION_raw_value = int(WIND_DIRECTION_hex_string, 16);
    wind_direction_1 = (WIND_DIRECTION_raw_value >> 3) & 1 ;
    WIND_DIRECTION_raw_value >>= 4;
    if(wind_direction_1):
        WIND_DIRECTION_raw_value |= 0x100
    return WIND_DIRECTION_raw_value

def wind_speed(raw_hex_data):
    WIND_SPEED_hex_string = raw_hex_data[12:14];
    return round(int(WIND_SPEED_hex_string,16) / 8 * 1.12, 2);

def air_temperature(raw_hex_data):
    AIR_TEMPERATURE_hex_string = raw_hex_data[7:10]
    AIR_TEMPERATURE_raw_value = int(AIR_TEMPERATURE_hex_string, 16);
    AIR_TEMPERATURE_raw_value <<= 1
    AIR_TEMPERATURE_raw_value >>= 1
    return ( AIR_TEMPERATURE_raw_value - 400 ) / 10;

def humidity(raw_hex_data):
    HUMIDITY_hex_string = raw_hex_data[10:12];
    return int(HUMIDITY_hex_string,16);

def gust_speed(raw_hex_data):
    GUST_SPEED_hex_string = raw_hex_data[14:16];
    return round(int(GUST_SPEED_hex_string,16) * 1.12, 2);

def accumulated_rainfall(raw_hex_data):
    ACCUMULATED_RAINFALL_hex_string = raw_hex_data[16:20];
    return round(int(ACCUMULATED_RAINFALL_hex_string,16) * 0.3, 2);

def uv(raw_hex_data):
    UV_hex_string = raw_hex_data[20:24];
    UV = int(UV_hex_string,16);
    
    if UV <= 432 :
        UVIndex = 0
    elif UV >= 433 and UV <= 851:
        UVIndex = 1
    elif UV >= 852 and UV <= 1210:
        UVIndex = 2
    elif UV >= 1211 and UV <= 1570:
        UVIndex = 3
    elif UV >= 1571 and UV <= 2017:
        UVIndex = 4
    elif UV >= 2018 and UV <= 2450:
        UVIndex = 5
    elif UV >= 2451 and UV <= 2761:
        UVIndex = 6
    elif UV >= 2762 and UV <= 3100:
        UVIndex = 7
    elif UV >= 3101 and UV <= 3512:
        UVIndex = 8
    elif UV >= 3513 and UV <= 3918:
        UVIndex = 9
    elif UV >= 3919 and UV <= 4277:
        UVIndex = 10
    elif UV >= 4278 and UV <= 4650:
        UVIndex = 11
    elif UV >= 4651 and UV <= 5029:
        UVIndex = 12
    else :
        UVIndex = 13
    return UVIndex;

def light(raw_hex_data):
    LIGHT_hex_string = raw_hex_data[24:30];
    return int(LIGHT_hex_string,16)/10;

def air_pressure(raw_hex_data):
    AIR_PRESSURE_hex_string = raw_hex_data[34:40];
    return int(AIR_PRESSURE_hex_string,16)/100; 

try:
    print(datetime.datetime.now());
    time.sleep(60);
    ser.open();
    WEATHER_STATION_raw_reading = "";
    print("ser is open");
except Exception as ex:
    print(datetime.datetime.now())
    print("open serial port error " + str(ex))
    exit()
    
try:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username="Muselab",password="Muselab1234")
#    client.connect("218.253.145.198", 18088, 60)
    client.connect("13.228.53.179", 1883, 60)
    client.loop_start();
    print("mqtt connected");
except Exception as ex:
    print("MQTT client connection error " + str(ex))
#    client.connect("218.253.145.198", 18088, 60)
    client.connect("13.228.53.179", 1883, 60)
    pass;
    #exit()
    

''' main logic '''
while ser.isOpen():
    #try:
        if (ser.in_waiting):
            WEATHER_STATION_raw_reading = ser.read(21).hex();
            print('xd')

            
        if( len(WEATHER_STATION_raw_reading) == 42 ):
            print("===============================")
            print("time: ", datetime.datetime.now()  )                
            print("raw_reading: ", WEATHER_STATION_raw_reading);
            
            WIND_DIRECTION = wind_direction(WEATHER_STATION_raw_reading);
            WIND_SPEED = wind_speed(WEATHER_STATION_raw_reading);
            HUMIDITY = humidity(WEATHER_STATION_raw_reading);
            AIR_TEMPERATURE = air_temperature(WEATHER_STATION_raw_reading);
            GUST_SPEED = gust_speed(WEATHER_STATION_raw_reading);
            ACCUMULATED_RAINFALL = accumulated_rainfall(WEATHER_STATION_raw_reading);
            UV = uv(WEATHER_STATION_raw_reading);
            LIGHT = light(WEATHER_STATION_raw_reading);
            AIR_PRESSURE = air_pressure(WEATHER_STATION_raw_reading);
            
            WEATHER_STATION_READING = {};
            #WEATHER_STATION_READING["WIND_DIRECTION"] = WIND_DIRECTION;
            #WEATHER_STATION_READING["WIND_SPEED"] = WIND_SPEED;
            WEATHER_STATION_READING["HUMIDITY"] = HUMIDITY;
            WEATHER_STATION_READING["AIR_TEMPERATURE"] = AIR_TEMPERATURE;
            #WEATHER_STATION_READING["GUST_SPEED"] = GUST_SPEED;
            #WEATHER_STATION_READING["ACCUMULATED_RAINFALL"] = ACCUMULATED_RAINFALL;
            WEATHER_STATION_READING["UV"] = UV;
            WEATHER_STATION_READING["LIGHT"] = LIGHT;
            #WEATHER_STATION_READING["AIR_PRESSURE"] = AIR_PRESSURE;
            
            print("WEATHER_STATION_READING: ", WEATHER_STATION_READING);
            #client.reconnect();
            client.publish("AquaFarm/Set1/Weather/Value", json.dumps(WEATHER_STATION_READING))
            #client.disconnect();
            WEATHER_STATION_raw_reading = "";
            
                
'''
    except Exception as ex:
        print("Station error: " + str(ex));ERROR = {};
        ERROR["ERROR"] = str(ex);
#        client.publish("AquaFarm/HongKong/Weather/Error", json.dumps(ERROR))
        print(ERROR)
#        time.sleep(120);
        pass;
'''
