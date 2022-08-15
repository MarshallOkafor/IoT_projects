"""
Original Author: LeMaRiva
Adopted and further modified by: Group 2 (Marshall, Ajay and Anjani) IoT Summer Course

Description: Simulated weather station using LoRa, ESP32 device, MQTT broker and Node-red
             
"""

import time
import ssd1306
import BME280
import config_lora
from machine import Pin, I2C
from time import sleep
import random
import json

# Device ID
device_id = config_lora.get_nodename()

"""
These lines of code are disabled since there is no physical sensor connected to ESP32

# ESP32 Sensor - Pin assignment
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)
bme = BME280.BME280(i2c=i2c)
"""

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


def temperature():
  
  # Randomly generated temperature readings
  
  t = random.uniform(20.00, 50.00)
  temp = '{:.2f}'.format(t)
  return temp

def humidity():
  """
  Randomly generated humidity readings
  """
  h = random.uniform(30.00, 70.00)
  hum = float("{:.2f}".format(h))
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
   

    return float(temp), float(hum), float(pres)
    
  except OSError as e:
    return('Failed to read sensor.')

def getCurrentTime(someTime):
    """
    Get current date and time
    """
    date = ''
    time = ''

    for i in range(0, 3):
        if i == 2:
            date += str(someTime[i])
        else:
            date += str(someTime[i]) + '-'

    for i in range(3, 6):
        if i == 5:
            time += str(someTime[i])
        else:
            time += str(someTime[i]) + ':'

    return date + ' ' + time

# Code to update the receiver
def send(lora):
    
    print('LoRa Temperature Sender\n')

    while True:
        date_time = getCurrentTime(time.localtime())
        print('Measuring weather conditions... ', end="")
        print('Reporting to LoRa Receiver.\n')

        temp, hum, pres = read_bme_sensor()

        payload = json.dumps({
            'dateTime': date_time,
            'deviceId': device_id, 
            'temp': temp,   
            'hum': hum,      
            'pres': pres
            })

        print("Sending packet: \n")
        print(payload)
        oled.text('Sending Data...', 0, 0)
        oled.text(date_time, 0, 10)
        oled.text('Temp: ' + str(temp) + 'C', 0, 20)
        oled.text('Hum: ' + str(hum) + '%', 0, 30)
        oled.text('Pres: ' + str(pres) + 'hPa', 0, 40)
        oled.show()

        lora.println(payload)

        
        oled.fill(0)
        sleep(5)
