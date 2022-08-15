"""
Original Author: LeMaRiva
Adopted and further modified by: Group 2 (Marshall, Ajay and Anjani) IoT Summer Course

Description: Simulated weather station using LoRa, ESP32 device, MQTT broker and Node-red
             
"""
# This code should be stored on the Receiver device
import LoRaReceiver
import config_lora
from sx127x import SX127x
from controller_esp32 import ESP32Controller

controller = ESP32Controller()

lora = controller.add_transceiver(SX127x(name = 'LoRa'),
                                  pin_id_ss = ESP32Controller.PIN_ID_FOR_LORA_SS,
                                  pin_id_RxDone = ESP32Controller.PIN_ID_FOR_LORA_DIO0)


LoRaReceiver.receive(lora)