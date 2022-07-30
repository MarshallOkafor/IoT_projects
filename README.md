# LED Lighting Using ESP32 and MQTT
-----------------------------------
In this project, we implemented an LED lighting control using ESP32, Mosquitto MQTT broker and Node-Red. The ESP32 device is configured and connected 
to the MQTT broker as a publisher and a subscriber. The broker is implemented using the popular mosquitto open source MQTT broker. Mosquitto was installed 
on a raspberry Pi. The network configuration of the broker was also modified to allow anonymous connection request from outside the raspberry Pi.

Node-Red, the popular JavaScript flows framework was configured and set up as a publisher client to control the LED on the ESP32. The LED is 
connected to the ESP32 through a breadboard. Any MQTT client can be used to publish ON and OFF string messages to control the LED.

The following steps below outline how to set up and use the application.
