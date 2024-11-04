from machine import Pin
import time
from wifi import conectar         #file .py
from sensor_umidade.dht11 import readDHT11    #file .py
from umqtt.simple import MQTTClient

"""
#                   Almir                                 Rafael                                    Stefano
clientid = ["aa07e300-803f-11ea-883c-638d8ce4c23d", "bf401e30-a656-11ea-93bf-d33a96695544", "a2c20010-a657-11ea-883c-638d8ce4c23d"]
# channels PUB
channel = ["1","2","3"]
# channels SUB
channel = ["5","6","7"]
"""
# Cayenne Definition
server = "mqtt.mydevices.com"
clientid = "a2c20010-a657-11ea-883c-638d8ce4c23d"
username = "d6033960-7df0-11ea-a67f-15e30d90bbf4"
password = "99e45f8e4ef9ef46f3bc0c42e4d0317e5bb523cb"

led = Pin(2, Pin.OUT)       # on ESP12E (not ESP32), LED is in GPIO 2
rele = Pin(23, Pin.OUT)
rele.value(1)                # on ESP12E (not ESP32), LED is off with level HIGH
rele.value(0)
type = "temp"
unit = "c"
channel = 3
channelSub = 7
temperatura = readDHT11()
topicPub = ("v1/%s/things/%s/data/%s" % (username, clientid, channel))
topicSub = ("v1/%s/things/%s/cmd/%s" % (username, clientid, channelSub))

conectar()          #wifi
#c.disconnect()       #if previously connected to cayenne
c = MQTTClient(clientid,server,0,username,password)
c.connect()

# sending data to channel
def pub():
  message = ("%s,%s=%s" %(type,unit,temperatura))
  c.publish(topicPub,message)
  print("Enviado:", temperatura)
  led.value(not led.value())
  time.sleep(0.2)
  led.value(not led.value())
  if int(temperatura) <= 30:
      time.sleep(2)
      rele.value(1)
  else:
      rele.value(0)  
  
#receiving data from channel
def sub():
  def sub_cb(topic, msg):
    p = msg.decode().split(',')
    print('Recebido: ',p[1])
    #sending status
    c.publish("v1/%s/things/%s/digital/%s" % (username, clientid, channelSub),"%s" %(p[1]))
    #sending actuator is ok
    c.publish("v1/%s/things/%s/response" % (username, clientid),"ok,%s" %(p[0]))
    # code to act on relay
    
    if str(p[1]) == "1" :    
        rele.value(1)      #turn relay ON
    else:    
        rele.value(0)
  
  c.set_callback(sub_cb)
  c.subscribe(topicSub)

while True:
  sub()
  time.sleep(0.1)
  pub()
  time.sleep(2)

