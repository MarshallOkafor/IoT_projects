# Overview
This application functions as a LoRa-based weather station. It consists of two LoRa nodes that communicate peer-to-peer. One node is the **sender**, attached to a BME680 environmental sensor. The other node is the **receiver**, acting as a gateway, which forwards the received data to an MQTT broker server.

# Prerequisites
* Heltec esp32 boards with LoRa v2.
* BME680 environment sensor.
* [Thonny](https://thonny.org/) IDE.

# Setup
1. Clone this repository.
2. Save the `sender` directory to the LoRa-enabled microcontroller board designated as the sender node. Similarly, save the `receiver` directory to the board designated as the receiver node.
3. Connect the sender node to the BME680 sensor using a breadboard and jumper wires. Refer to the microcontroller board's datasheet for accurate GPIO connections.
4. Power up both nodes by connecting them to a computer. Ensure to check the ```/dev```(on Linux OS) interfaces for their connections. Separate computers can be used for each board.
5. Install the Thonny IDE to communicate with the boards and run the code.

# Test the application
1. Using Thonny, connect to the sender LoRa node. Enter the command below on the Micropython REPL:
```
from sender import main
```
The sender node will start transmitting environmental data, including ```temp```, ```hum```, ```pres```, and ```VOC gas``` over LoRa.
2. Similarly, connect to the receiver LoRa node and run:
```
from receiver import main
```
The receiver will start obtaining the environmental data through LoRa.

**Note:** By default, the receiver acts as both a gateway and an MQTT client. If you don't have an MQTT broker setup, you may either set one up or comment out lines 40-68 in the ```LoRaReceiver.py``` file, which handles the MQTT data publishing.