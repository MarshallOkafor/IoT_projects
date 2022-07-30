# Summer IoT Course 2022
========================

This repository contains some of the IoT projects we implemented during our IoT 2022 Summer course.

## LED Lighting Using ESP32 and MQTT
-----------------------------------
In this project, we implemented an LED lighting control using ESP32, Mosquitto MQTT broker and Node-Red. The ESP32 device is configured and connected 
to the MQTT broker as a publisher and a subscriber. The broker is implemented using the popular mosquitto open source MQTT broker. Mosquitto was installed 
on a raspberry Pi. The network configuration of the broker was also modified to allow anonymous connection request from outside the raspberry Pi.

Node-Red, the popular JavaScript flows framework was configured and set up as a publisher client to control the LED on the ESP32. The LED is 
connected to the ESP32 through a breadboard. Any MQTT client can be used to publish ON and OFF string messages to control the LED.

The following steps below outline how to set up and use the application.

## Weather Station Using BME280 Sensor and Node-red 
---------------------------------------------------
We implemented a weather station using randomly generated readings due to the absence of a physical BME sensor at the time of writing the code. The codes were however neatly written to allow the connection of a BME sensor. All you have to do, uncomment some of the lines that are meant to connect and read from the BME280 device. Please read the comments on the code for futher clarity on this.

Simulated reading from the ESP32 device are published to a Mosquitto MQTT broker. A simpled dashboard was created using Node-red. the publsihed readings are then displayed on the Node-red dashboard.
