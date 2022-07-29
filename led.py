"""

Original Author: Pi4IoT
Adopted and further modified by: Group 2 (Marshall, Ajay and Anjani) IoT Summer Course

Description: Micropython code to connect ESP32 device to a broker
             Publish a topic and subscribe to a topic

"""

from umqtt.simple import MQTTClient
from machine import Pin
import machine
import ubinascii
 
# Setup a GPIO Pin for output
led = Pin(32, Pin.OUT)

# Configure the connection to the broker
CONFIG = {
     # Configuration details of the MQTT broker
     "MQTT_BROKER": "192.168.0.108",
     "USER": "",
     "PASSWORD": "",
     "PORT": 1883,
     "TOPIC": b"test",
     # unique identifier of the ESP32 chip
     "CLIENT_ID": b"esp32_" + ubinascii.hexlify(machine.unique_id())
}
 
# Method to act based on message received   
def onMessage(topic, msg):
    print("Topic: %s, Message: %s" % (topic, msg))
 
    if msg == b"on":
        led.on()
    elif msg == b"off":
        led.off()
 
def listen():
    #Create an instance of MQTTClient 
    client = MQTTClient(CONFIG['CLIENT_ID'], CONFIG['MQTT_BROKER'], user=CONFIG['USER'], password=CONFIG['PASSWORD'], port=CONFIG['PORT'])
    # Attach call back handler to be called on receiving messages
    client.set_callback(onMessage)
    client.connect()
    client.publish("test", "ESP32 is Connected")
    client.subscribe(CONFIG['TOPIC'])
    print("ESP32 is Connected to %s and subscribed to %s topic" % (CONFIG['MQTT_BROKER'], CONFIG['TOPIC']))
 
    try:
        while True:
            msg = client.wait_msg()
    finally:
        client.disconnect()  

listen()        