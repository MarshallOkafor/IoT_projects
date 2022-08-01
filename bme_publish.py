"""

Original Author: Randomnerdtutorials
Adopted and further modified by: Group 2 (Marshall, Ajay and Anjani) IoT Summer Course

Description: Simulated weather station using ESP32 device, MQTT broker and Node-red
             
"""

import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import micropython
import esp
import BME280
from machine import Pin, I2C
import random
import datetime

esp.osdebug(None) # Turnoff vendor debugging message

# import gc
# gc.collect()

"""
These lines of code are disabled since there is no physical sensor connected to ESP32

# ESP32 - Pin assignment
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)
bme = BME280.BME280(i2c=i2c)
"""

# Configure the connection to the broker
CONFIG = {
     # Configuration details of the MQTT broker
     "MQTT_BROKER": "192.168.0.108",
     "USER": "",
     "PASSWORD": "",
     "PORT": 1883,
     "TOPIC_TEMP": b"esp/bme280/temperature",
     "TOPIC_HUM": b"esp/bme280/humidity",
     "TOPIC_PRES": b"esp/bme280/pressure",
     # unique identifier of the ESP32 chip
     "CLIENT_ID": b"esp32_" + ubinascii.hexlify(machine.unique_id())
}

# Variables to keep track of publishing times
last_message = 0
message_interval = 5


def connect_mqtt():
  #Create an instance of MQTTClient 
  client = MQTTClient(CONFIG['CLIENT_ID'], CONFIG['MQTT_BROKER'], user=CONFIG['USER'], 
           password=CONFIG['PASSWORD'], port=CONFIG['PORT'])
  
  client.connect()
  print('Connected to %s MQTT broker' % (CONFIG['MQTT_BROKER']))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()
  import wlan

def temperature():
  """
  Randomly generated temperature readings
  """
  t = random.uniform(20.00, 50.00)
  temp = "{:.2f}".format(t)
  return temp

def humidity():
  """
  Randomly generated humidity readings
  """
  h = random.uniform(30.00, 70.00)
  hum = "{:.2f}".format(h)
  return hum

def pressure():
  """
  Randomly generated pressure readings
  """
  p = random.uniform(500.00, 1000.00)
  pres = "{:.2f}".format(p)
  return pres

def read_bme_sensor():
  try:
    """
    These lines of code are disabled since there is no physical sensor connected to ESP32

    temp = b'%s' % bme.temperature[:-1]
    hum = b'%s' % bme.humidity[:-1]
    pres = b'%s'% bme.pressure[:-3]
    """

    # Hard-coded sensor readings as test readings
    temp = b'%s' % temperature()
    hum = b'%s' % humidity()
    pres = b'%s' % pressure()

    return temp, hum, pres
    
  except OSError as e:
    return('Failed to read sensor.')

try:
  client = connect_mqtt()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    if (time.time() - last_message) > message_interval:
      temp, hum, pres = read_bme_sensor()
      print(temp)
      print(hum)
      print(pres)
      client.publish(CONFIG["TOPIC_TEMP"], temp)
      client.publish(CONFIG["TOPIC_HUM"], hum)      
      client.publish(CONFIG["TOPIC_PRES"], pres)
      ct = str(datetime.datetime.now())
      n=0
      while n < 11:
        with open('recordings.txt','w') as f:
          f.write(ct)
          f.write(temperature())
          f.write(pressure())
          f.write(humidity())
          n+=1
        
      last_message = time.time()
  except OSError as e:
    restart_and_reconnect()