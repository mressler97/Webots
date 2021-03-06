#Nicholas Dzomba and Michael Resller
#CSCI 455 Final Project Controller

from controller import Robot, Compass
import math, sys
from math import pi as M_PI

TIME_STEP = 64
robot = Robot()
compass = Compass("compass")
compass.enable(TIME_STEP)

ds = []
dsNames = ['ds_right', 'ds_left']


wheels = []
wheelsNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']

avoidObstacleCounter = 0
finstate = 0
start_state = 1
turnCounter = 0.0

for i in range(2):
    ds.append(robot.getDistanceSensor(dsNames[i]))
    ds[i].enable(TIME_STEP)

for i in range(4):
    wheels.append(robot.getMotor(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)
    

# calculate bearing from compass vector list    
def get_bearing_in_degrees():
    north = compass.getValues()
    rad = math.atan2(north[0], north[2])
    bearing = (rad - 1.5708) / M_PI * 180.0
    if (bearing < 0.0):
        bearing = bearing + 360.0;
    return bearing
    
# set speeds of motors    
def set_motor_speed(wheels, leftSpeed, rightSpeed):
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(rightSpeed)
    wheels[2].setVelocity(leftSpeed)
    wheels[3].setVelocity(rightSpeed)
    


while robot.step(TIME_STEP) != -1:
    direction = get_bearing_in_degrees()
    print(direction)
    if turnCounter <= 1: #go straight
        leftSpeed = 2.0
        rightSpeed = 2.0
        turnCounter += 0.02
    if 1 < turnCounter < 2: 
        turnCounter = 2
    if 1 < turnCounter < 10: #make right turn
        if turnCounter % 2 == 0:
            leftSpeed = 2.4
            rightSpeed = 0.75
            if 90 > direction > 45:
                turnCounter += 1                        
        else: # make left turn
            if finstate == 0:
                leftSpeed = 0.75
                rightSpeed = 2.4
            else:
                if direction >= 358:
                    turnCounter = 100
                else:
                    leftSpeed = 2.4
                    rightSpeed = 0.75
            if 270 < direction < 315:
                if turnCounter != 9:
                    turnCounter += 1
                else:
                    finstate = 1           
    else: # go straight again
        leftSpeed = 2.0
        rightSpeed = 2.0
    if avoidObstacleCounter > 0: # stop before wall
        avoidObstacleCounter -= 1
        leftSpeed = 0.0
        rightSpeed = 0.0
        set_motor_speed(wheels, leftSpeed, rightSpeed)
        compass.disable()
        print("Complete!")
        sys.exit(0)
    else:  # set speeds if no wall
        for i in range(2):
            if ds[i].getValue() < 950.0:
                avoidObstacleCounter = 100
                
    set_motor_speed(wheels, leftSpeed, rightSpeed)

    

   
