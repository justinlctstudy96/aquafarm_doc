# Amazon EC2 PORTs
PURPOSE                 PORT
Grafana                 3000
InfluxDb                8086
Nodejs Camera Server    8080
MQTT Broker             1883

# Amazon EC2 SSH
ssh ubuntu@muselabs-aquafarm
Host muselabs-aquafarm
  Hostname 13.228.53.179
  User ubuntu
  IdentityFile ~/.ssh/muselabs-AquaFarm.pem

# Grafana Users
User        Password        Role
Muselab     Muselabs1234    Primary user
William     William1234     User
Tracy       Tracy1234

# InfluxDb Users
User        Password        Role
Muselab     Muselab1234     Primary user
William     William1234     User

Primary organization name: AquaGreen
Bucket Name: AquaFarm
Retention Period: 0, infinite

# Nodejs Camera Server APIs
app.get('/');
app.get('/latest/:camera');
app.get('/:camera/:time');
app.post('/upload/camera0');
app.post('/upload/camera1');

# MQTT Users:
User        Password
Muselab     Muselab1234
AquaGreen   vegetarian
Set1        Set11234
Set2        Set21234
Set3        Set31234
Set1Pi      Set1Pi1234
Set2Pi      Set2Pi1234
Subscriber1 Subscriber11234
Subscriber2 Subscriber21234
Subscriber3 Subscriber31234
Publisher1  Publisher11234
Publisher2  Publisher21234
Publisher3  Publisher31234
InfluxUser  InfluxUser1234
mqttLens    mqttLens1234
Telegraf    Telegraf1234

# Client Raspberry Pi 4B _ set1
Name: AquaGreen
Computer: aquagreen-desktop
password: aquagreen 


# VM startup
vboxmanage startvm "AquaGreen" --type=headless 
