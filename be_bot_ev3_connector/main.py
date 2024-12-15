#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile



# Create your objects here.
ev3 = EV3Brick()

obstacle_sensor = InfraredSensor(Port.S4)
# Write your program here.
ev3.speaker.beep()

left_motor = Motor(Port.A)
right_motor = Motor(Port.D)


robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=160)


while True:
    
    while obstacle_sensor.distance() > 20:
        ev3.screen.print(obstacle_sensor.distance())
        robot.drive(-200, 0)
        wait(5)
    
    robot.straight(50)
    robot.turn(700)
    wait(5)

