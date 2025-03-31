#!/usr/bin/env python
import rospy
import serial
from std_msgs.msg import Float32MultiArray

# Configure serial communication
UART_PORT = "/dev/ttyUSB0"  # Change to your UART device
BAUD_RATE = 9600
MOTOR_IDS = [0x01, 0x02, 0x03, 0x04]  # Motor IDs (1 to 4)

# Initialize serial connection
try:
    ser = serial.Serial(UART_PORT, BAUD_RATE, timeout=1)
    rospy.loginfo(f"Connected to SD02C motor driver on {UART_PORT}")
except serial.SerialException:
    rospy.logerr("Failed to connect to UART device.")
    exit(1)

def compute_checksum(data):
    """Compute checksum (sum of bytes mod 256)"""
    return sum(data) % 256

def send_motor_command(motor_id, speed):
    """
    Send UART command to SD02C to control motor speed and direction.
    Speed range: -100 (full reverse) to 100 (full forward)
    """
    direction = 0x00 if speed >= 0 else 0x80  # Forward (0x00) / Reverse (0x80)
    abs_speed = min(abs(int(speed)), 100)  # Clamp speed to max 100
    speed_byte = direction | abs_speed  # Merge direction and speed

    # UART packet: [Start Byte, Motor ID, Command, Speed, Checksum]
    command_packet = [0xA5, motor_id, 0x02, speed_byte]
    checksum = compute_checksum(command_packet)
    command_packet.append(checksum)

    # Send command
    ser.write(bytearray(command_packet))
    rospy.loginfo(f"Motor {motor_id}: Sent {command_packet}")

def motor_callback(msg):
    """
    ROS Subscriber Callback:
    Receives Float32MultiArray and sends UART commands for 4 motors.
    """
    if len(msg.data) != 4:
        rospy.logwarn("Received incorrect motor data length. Expected 4 values.")
        return
    
    for i in range(4):
        send_motor_command(MOTOR_IDS[i], msg.data[i])


if __name__ == "__main__":
    rospy.init_node("motor_controller", anonymous=True)
    rospy.Subscriber("/motor_cmd", Float32MultiArray, motor_callback)
    rospy.loginfo("SD02C Multi-Motor ROS Node Initialized. Listening for /motor_cmd...")
    rospy.spin()
