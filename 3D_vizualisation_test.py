import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Phidget22.Devices.Spatial import *
from Phidget22.Devices.Accelerometer import *
from Phidget22.Devices.Gyroscope import *
from Phidget22.Devices.Magnetometer import *
import time

vertices = [
    [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
    [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
]

edges = [(0,1), (1,2), (2,3), (3,0),
         (4,5), (5,6), (6,7), (7,4),
         (0,4), (1,5), (2,6), (3,7)]

def draw_cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def onAccelerationChange(self, acceleration, timestamp):
    global angle_x, angle_y, angle_z
    angle_x = acceleration[0]
    angle_z = acceleration[1]
    angle_y = 0

pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0, 0, -5)

angle_x, angle_y, angle_z = 0, 0, 0
running = True

#Create the Phidget channels
accelerometer0 = Accelerometer()
#Assign any event handlers before calling open so that no events are missed.
accelerometer0.setOnAccelerationChangeHandler(onAccelerationChange)
#Open your Phidgets and wait for attachment
accelerometer0.openWaitForAttachment(5000)

while running:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)
    glRotatef(angle_z, 0, 0, 1)

    draw_cube()
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
