#!/usr/bin/env python3

import rospy
import socket
from std_msgs.msg import String, Float32MultiArray
import struct

def log_data(acceleration, angularRate, magneticField, timestamp):
    acceleration_msg = "Acceleration: \t"+ str(acceleration[0])+ "  |  "+ str(acceleration[1])+ "  |  "+ str(acceleration[2]) + "\n"
    angular_msg = "AngularRate: \t"+ str(angularRate[0])+ "  |  "+ str(angularRate[1])+ "  |  "+ str(angularRate[2]) + "\n"
    magnetic_msg = "MagneticField: \t"+ str(magneticField[0])+ "  |  "+ str(magneticField[1])+ "  |  "+ str(magneticField[2]) + "\n"
    timestamp_msg = "Timestamp: " + str(timestamp) + "\n"
    rospy.loginfo("Received: \n" + acceleration_msg + angular_msg + magnetic_msg + timestamp_msg)

def socket_server():
    rospy.init_node('socket_server_node', anonymous=True)
    pub = rospy.Publisher('socket_data', Float32MultiArray, queue_size=10)

    HOST = "0.0.0.0"
    PORT = 5000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    rospy.loginfo("Socket server running on port 5000...")
    conn, addr = server.accept()
    rospy.loginfo(f"Connected to {addr}")

    while not rospy.is_shutdown():
        data = conn.recv(1024).decode()
        if data:
            unpacked_data = struct.unpack("9f1d", data)
            acceleration = unpacked_data[0:3]
            angularRate = unpacked_data[3:6]
            magneticField = unpacked_data[6:9]
            timestamp = unpacked_data[9]
            log_data(acceleration, angularRate, magneticField, timestamp)

            # Publish as ROS message
            msg = Float32MultiArray()
            msg.data = list(acceleration + angularRate + magneticField + (timestamp,))
            pub.publish(msg)

    conn.close()

if __name__ == "__main__":
    try:
        socket_server()
    except rospy.ROSInterruptException:
        pass
