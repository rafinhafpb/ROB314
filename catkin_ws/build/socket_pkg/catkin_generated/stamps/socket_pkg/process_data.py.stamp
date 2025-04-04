#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32MultiArray
import numpy as np

def callback(msg):
    data = np.array(msg.data)

    # Extract acceleration and scale it
    acceleration = 100 * data[:3]  # X, Y, Z
    angular_rate = data[3:6]       # X, Y, Z
    timestamp = data[9]            # Single float value

    acc_x, acc_y = acceleration[0], acceleration[1]
    acc_magnitude = np.hypot(acc_x, acc_y)  # sqrt(x² + y²)

    motor_speeds = np.zeros(4)

    # Detects tilts that are higher than a threshold from resting position
    if abs(acceleration[2]) <= 95:
        # Move left/right
        if abs(acc_x) > 10 and abs(acc_y) < 10:
            motor_speeds = [acc_x, -acc_x, -acc_x, acc_x]

        # Move forward/backward
        elif abs(acc_x) < 10 and abs(acc_y) > 10:
            motor_speeds = [acc_y, acc_y, acc_y, acc_y]

        # Move diagonally
        elif abs(acc_x) > 10 and abs(acc_y) > 10:
            if acc_x > 0 and acc_y > 0:  # Forward-left
                motor_speeds = [0, acc_magnitude, acc_magnitude, 0]
            elif acc_x > 0 and acc_y < 0:  # Backward-left
                motor_speeds = [-acc_magnitude, 0, 0, -acc_magnitude]
            elif acc_x < 0 and acc_y > 0:  # Forward-right
                motor_speeds = [acc_magnitude, 0, 0, acc_magnitude]
            elif acc_x < 0 and acc_y < 0:  # Backward-right
                motor_speeds = [0, -acc_magnitude, -acc_magnitude, 0]

    # Publish motor speeds
    pub.publish(Float32MultiArray(data=motor_speeds))

def listener():
    rospy.init_node('process_data', anonymous=True)
    global pub
    pub = rospy.Publisher('/motor_cmd', Float32MultiArray, queue_size=10)
    rospy.Subscriber('socket_data', Float32MultiArray, callback)  # Ensure correct type!
    
    rospy.loginfo("Motor control node started. Listening for data...")
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
