#Nicholas Dzomba and Michael Resller
#CSCI 455 Final Project Controller

from controller import Robot, Compass
import math
from math import pi as M_PI

TIME_STEP = 64
robot = Robot()
compass = Compass("compass")

ds = []
dsNames = ['ds_right', 'ds_left']

compass.enable(TIME_STEP)

def get_bearing_in_degrees():
    north = compass.getValues()
    rad = math.atan2(north[0], north[2])
    bearing = (rad - 1.5708) / M_PI * 180.0
    if (bearing < 0.0):
        bearing = bearing + 360.0;
    return bearing
    

for i in range(2):
    ds.append(robot.getDistanceSensor(dsNames[i]))
    ds[i].enable(TIME_STEP)
wheels = []
wheelsNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']
for i in range(4):
    wheels.append(robot.getMotor(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)
avoidObstacleCounter = 0
turnCounter = 0
while robot.step(TIME_STEP) != -1:
    direction = get_bearing_in_degrees()
    print(direction)
    if 0 < turnCounter < 8:
        if turnCounter % 2 == 0:
            leftSpeed = 1.6
            rightSpeed = 0.5
            if 90 > direction > 45:
                turnCounter += 1      
        else:
            leftSpeed = 0.5
            rightSpeed = 1.6
            if 270 < direction < 315:
                turnCounter += 1
                
    else:
        leftSpeed = 1.5
        rightSpeed = 1.5
    if avoidObstacleCounter > 0:
        avoidObstacleCounter -= 1
        leftSpeed = 0.0
        rightSpeed = 0.0
    else:  # read sensors
        for i in range(2):
            if ds[i].getValue() < 950.0:
                avoidObstacleCounter = 100
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(rightSpeed)
    wheels[2].setVelocity(leftSpeed)
    wheels[3].setVelocity(rightSpeed)
    direction = get_bearing_in_degrees() 
    print(direction)
    

   
