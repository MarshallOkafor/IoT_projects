"""
Original Author: LeMaRiva
Adopted and further modified by: Group 2 (Marshall, Ajay and Anjani) IoT Summer Course

Description: Simulated weather station using LoRa, ESP32 device, MQTT broker and Node-red
             
"""

import ssd1306
from machine import Pin, I2C
from umqtt.simple import MQTTClient
import ubinascii
import machine
import time

# Heltec LoRa 32 with OLED Display
oled_width = 128
oled_height = 64

# OLED reset pin
i2c_rst = Pin(16, Pin.OUT)

# Initialize the OLED display
i2c_rst.value(0)
time.sleep_ms(5)
i2c_rst.value(1) # must be held high after initialization

# Setup the I2C lines
i2c_scl = Pin(15, Pin.OUT, Pin.PULL_UP)
i2c_sda = Pin(4, Pin.OUT, Pin.PULL_UP)

# Create the bus object
i2c = I2C(scl=i2c_scl, sda=i2c_sda)

# Create the display object
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
oled.fill(0)

# Configure the connection to the broker
CONFIG = {
     # Configuration details of the MQTT broker
     "MQTT_BROKER": "192.168.2.3",
     "USER": "",
     "PASSWORD": "",
     "PORT": 1883,
     "TOPIC_WEATHER": b"LoRa/data",
     # unique identifier of the ESP32 chip
     "CLIENT_ID": b"esp32_" + ubinascii.hexlify(machine.unique_id())
}

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

try:
  client = connect_mqtt()
except OSError as e:
  restart_and_reconnect()

def receive(lora):
    print("LoRa Weather Receiver\n")

    while True:
        if lora.receivedPacket():
            lora.blink_led()

            try:
                payload = lora.read_payload()
                print("*** Received New Weather Reading ***\n{}".format(payload.decode()))
                oled.text('Receiving Data...', 0, 0)
                print('Publishing New Data To Broker...')
                oled.text('Publishing...', 0, 10)
                oled.show()
                client.publish(CONFIG["TOPIC_WEATHER"], payload.decode())
                oled.text('DataPublished!', 0, 20)

            except Exception as e:
                print(e)
            oled.fill(0)    
            print("with RSSI: {}\n".format(lora.packetRssi))
