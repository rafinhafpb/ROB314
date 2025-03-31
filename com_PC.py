from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Spatial import *
from Phidget22.Devices.Accelerometer import *
from Phidget22.Devices.Gyroscope import *
from Phidget22.Devices.Magnetometer import *
import socket
import struct
import time

def onSpatialData(self, acceleration, angularRate, magneticField, timestamp):
    packed_data = struct.pack("9f1d", *(acceleration + angularRate + magneticField + [timestamp]))
    client.sendall(packed_data)

HOST = "192.168.134.195"  # Raspberry Pi's IP Address
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

spatial0 = Spatial()
spatial0.setOnSpatialDataHandler(onSpatialData)
spatial0.openWaitForAttachment(5000)

try:
    while True:
        pass

except KeyboardInterrupt:
    print("Closing communication port...")
    client.close()
    spatial0.close()
