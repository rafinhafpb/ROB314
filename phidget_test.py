# Verify installation and import packages
import importlib
import subprocess
import sys

try:
    importlib.import_module("Phidget22")
    print("Phidget22 is already installed.")
except ImportError:
    print("Phidget22 is not installed. Installing...")
    subprocess.check_call([sys.executable, "pip", "install", "Phidget22"])

from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Spatial import *
from Phidget22.Devices.Accelerometer import *
from Phidget22.Devices.Gyroscope import *
from Phidget22.Devices.Magnetometer import *
import time

def onSpatialData(self, acceleration, angularRate, magneticField, timestamp):
	print("Acceleration: \t"+ str(acceleration[0])+ "  |  "+ str(acceleration[1])+ "  |  "+ str(acceleration[2]))
	print("AngularRate: \t"+ str(angularRate[0])+ "  |  "+ str(angularRate[1])+ "  |  "+ str(angularRate[2]))
	print("MagneticField: \t"+ str(magneticField[0])+ "  |  "+ str(magneticField[1])+ "  |  "+ str(magneticField[2]))
	print("Timestamp: " + str(timestamp))
	print("----------")
	
def onAccelerationChange(self, acceleration, timestamp):
	print("Acceleration: \t"+ str(acceleration[0])+ "  |  "+ str(acceleration[1])+ "  |  "+ str(acceleration[2]))
	print("Timestamp: " + str(timestamp))
	print("----------")

def onAngularRateUpdate(self, angularRate, timestamp):
	print("AngularRate: \t"+ str(angularRate[0])+ "  |  "+ str(angularRate[1])+ "  |  "+ str(angularRate[2]))
	print("Timestamp: " + str(timestamp))
	print("----------")

def onMagneticFieldChange(self, magneticField, timestamp):
	print("MagneticField: \t"+ str(magneticField[0])+ "  |  "+ str(magneticField[1])+ "  |  "+ str(magneticField[2]))
	print("Timestamp: " + str(timestamp))
	print("----------")

def main():
	#Create the Phidget channels
	accelerometer0 = Accelerometer()
	gyroscope0 = Gyroscope()
	magnetometer0 = Magnetometer()
	spatial = Spatial()
	
	#Assign any event handlers before calling open so that no events are missed.
	accelerometer0.setOnAccelerationChangeHandler(onAccelerationChange)
	gyroscope0.setOnAngularRateUpdateHandler(onAngularRateUpdate)
	magnetometer0.setOnMagneticFieldChangeHandler(onMagneticFieldChange)

	#Open your Phidgets and wait for attachment
	accelerometer0.openWaitForAttachment(5000)
	gyroscope0.openWaitForAttachment(5000)
	magnetometer0.openWaitForAttachment(5000)
    

	# # Event handler when spatial data in received
	# spatial.setOnSpatialDataHandler(onSpatialData)

	# # Hold the program until a Phidget channel matching the one specified is attached, or the function times out.
	# spatial.openWaitForAttachment(5000)

	try:
		input("Press Enter to Stop\n")
	except (Exception, KeyboardInterrupt):
		pass

	spatial.close()

if __name__ == "__main__":
    main()