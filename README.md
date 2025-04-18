## ROB314 Project

This repository contains the codes used for the ROB314 project, which is the control of a four omnidirectional wheel robot using an IMU (Inertial Measurement Unit) for the directional command.
The robot is controlled by a Raspberry Pi with ROS and an Arduino for the motor control. An external notebook is used to acquire the IMU data and send it to the Raspberry Pi using Socket communication.
The IMU data is used to control the robot's direction, while the Raspberry Pi receives this data and controls the speed and direction of the motors, sending it to the Arduino, which finally converts them to PWM (Pulse Width Modulation) signals for each motor.
The next sections will guide you through the process on how to run the project, the dependencies, and the codes to be used.

### ROS Package Structure

Inside the Raspberry Pi, we used the Robot Operating System (ROS) to control the robot. The ROS version used is Noetic, which is compatible with Ubuntu 20.04. The installation of ROS Noetic can be found [here](http://wiki.ros.org/noetic/Installation/Ubuntu).

For the ROS workspace, we used the catkin tools to create the package structure. The tutorial to create a ROS workspace can be found [here](https://wiki.ros.org/ROS/Tutorials/InstallingandConfiguringROSEnvironment).

After creating the workspace, we created two packages named `robot_control` and `socket_pkg`, which are the packages used for the robot control and the socket communication, as well as the data transformation between the IMU data to speed and direction for the robot.
The commands to create the packages are as follows:

```bash
cd ~/catkin_ws/src
catkin_create_pkg robot_control std_msgs rospy serial
catkin_create_pkg socket_pkg std_msgs rospy socket
```

If either the installation of `serial` or `socket` fails, you can install them using the following command:

```bash
rosdep install --from-paths src --ignore-src -r -y
```

This command will install all the dependencies for the packages in the `src` folder.

After creating the packages, you can create the files for the codes. The files are located in the `src` folder of each package.

The `robot_control` package contains the code `motor_control.py`, which is the code used to send the speed ans direction to the Arduino, while the `socket_pkg` package contains the code `socket_server.py` and `process_data.py` which are the codes used to receive the IMU data from the external notebook, and convert the accelerometer measurements into speed and direction.

The `socket_server.py` code is the main code that runs the socket server and receives the data from the external notebook, publishing the raw data to the `/socket_data` topic. The `process_data.py` code subscribes to the `/socket_data` topic and treats the data, converting it into speed (the scalar value) and direction (the signal, either positive or negative), and publishing it to the `/motor_cmd` topic.

Finally, the `motor_control.py` code subscribes to the `/motor_cmd` topic and sends the speed and direction to the Arduino, which is connected to the Raspberry Pi using a USB cable. The Arduino receives the data and converts it into PWM signals for each motor.

In order to run all the nodes at the same time, we created a launch file names `start_nodes,launch` in the `robot_control` package. To run the launch file, use the following command:

```bash
roslaunch robot_control start_nodes.launch
```

If you want to run the nodes separately, you can use the following commands in different terminals, and make sure to run the `roscore` command in a separate terminal:

```bash
rosrun socket_pkg socket_server.py
rosrun socket_pkg process_data.py
rosrun robot_control motor_control.py
```

To listen to any of the topics, you can use the following command:

```bash
rostopic echo /topic_name
```

Where `topic_name` is the name of the topic you want to listen to.


### External Notebook

First of all, make sure to install the drivers to connect the IMU Phidget Spatial 3/3/3, which can be found [here](https://www.phidgets.com/?prodid=1205&srsltid=AfmBOopWggetKDQYZjtsqRIdu-7cVCgI0Am_0eBtSVFx5XCMFKcO_F6x#Tab_User_Guide).

The external notebook is used to acquire the IMU data and send it to the Raspberry Pi using Socket communication. The code used for the external notebook is the `com_PC.py` file. It uses the `socket` library, as well the Phidget library to connect to the IMU. To install the dependencies, use the following command:

```bash
pip install socket phidget22
```

After that, you should be able to run the code while connected to the IMU via USB. The code will acquire the IMU data and send it to the Raspberry Pi using Socket communication. The IP address and port number used for the Socket communication are defined in the code, so make sure to change them if necessary.

### Arduino

The Arduino code is used to receive the speed and direction from the Raspberry Pi throught Serial communication, and converti it into PWM signals for each motor. The code used for the Arduino is the `PWM_control_arduino.ino` file. The code does not use any external libraries, because the ports used are programmed using AnalogWrite.
Simply upload the code to the Arduino and connect it to the Raspberry Pi using a USB cable.

### Run the Project

To run the project, you can either interface with the Raspberry Pi using SSH or connect a monitor, mouse and keyboard to the Raspberry Pi.

Inside the terminal, run the launch file (as explained above), which will run all the nodes at the same time, including the socket server, which will wait for the connection from the external notebook.

After that, run the `com_PC.py` code in the external notebook, which will connect to the Raspberry Pi and start sending the IMU data. The IMU data will be published to the `/socket_data` topic, and the `process_data.py` code will convert it into speed and direction, publishing it to the `/motor_cmd` topic.
Finally, the `motor_control.py` code will subscribe to the `/motor_cmd` topic and send the speed and direction to the Arduino, which will convert it into PWM signals for each motor.

The robot should now be able to move in the direction commanded by the IMU data. You can test it by moving the IMU in different directions and observing the robot's movement.