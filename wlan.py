"""

Author: Group 2 (IoT Summer Course)

Description: Code to automatically connect the ESP32 to Wifi
             User will be prompted to enter the SSID and Password

"""

import network
import sys

# Initialize the network interface
station = network.WLAN(network.STA_IF)

# Confirm that the network interface is active
if station.active(True):
    print("Wireless card is now active!")
else:
    print("Failed to start the wireless card!")
    sys.exit()

# Connect the ESP32 device to the Wifi
station.connect(input("Enter Wifi SSID: "), input("Enter Wifi Password: "))

# Check if the connection was successful
if station.ifconfig():
    print("Connection to the Wifi was successful!")
    print("Your Wifi IP details are:")
    print(station.ifconfig())
else:
    print("Failed to connect to the Wifi!")
    print("Try again or check the network configuration script.")