from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Spatial import *
from Phidget22.Devices.Accelerometer import *
from Phidget22.Devices.Gyroscope import *
from Phidget22.Devices.Magnetometer import *
import socket
import time

def onAccelerationChange(self, acceleration, timestamp):
	data = "Acceleration: \t"+ str(acceleration[0])+ "  |  "+ str(acceleration[1])+ "  |  "+ str(acceleration[2])
	client.send(data.encode())

HOST = "192.168.134.195"  # Raspberry Pi's IP Address
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
accelerometer0 = Accelerometer()
accelerometer0.setOnAccelerationChangeHandler(onAccelerationChange)
accelerometer0.openWaitForAttachment(5000)

try:
    while True:
        pass

except KeyboardInterrupt:
    print("Closing communication port...")
    client.close()
    accelerometer0.close()
