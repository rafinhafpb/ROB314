#!/usr/bin/env python
import rospy
import serial
from std_msgs.msg import Float32MultiArray

# Configure serial communication
UART_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200

# Initialize serial connection
try:
    ser = serial.Serial(UART_PORT, BAUD_RATE, timeout=1)
    rospy.loginfo(f"Connected to SD02C motor driver on {UART_PORT}")
except serial.SerialException:
    rospy.logerr("Failed to connect to UART device.")
    exit(1)

def motor_callback(msg):
    """
    ROS Subscriber Callback:
    Receives Float32MultiArray and sends UART commands for 2 motors.
    """
    if len(msg.data) != 2:
        rospy.logwarn("Received incorrect motor data length. Expected 2 values.")
        return
    
    try:
        # Convert the list of floats to a comma-separated string
        data_to_send = ",".join(map(str, msg.data)) + "\n"
        ser.write(data_to_send.encode('utf-8'))
    except Exception as e:
        rospy.logerr(f"Failed to send data over UART: {e}")

if __name__ == "__main__":
    rospy.init_node("motor_controller", anonymous=True)
    rospy.Subscriber("/motor_cmd", Float32MultiArray, motor_callback)
    rospy.loginfo("SD02C Multi-Motor ROS Node Initialized. Listening for /motor_cmd...")
    
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Shutting down motor controller node.")
    finally:
        ser.close()
