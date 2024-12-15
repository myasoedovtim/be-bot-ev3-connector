#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from umqtt.robust import MQTTClient

#from pybricks.media.ev3dev import SoundFile, ImageFile


MQTT_ClientID = "1fa419a0-a9fa-4866-a1e2-a0e651ec0b29"
MQTT_HOST="m6.wqtt.ru"
MQTT_PORT=17810
MQTT_USER=""
MQTT_PASSWORD=""

client = MQTTClient(MQTT_ClientID, MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASSWORD)
client.connect()

client.publish("/robot/topic", MQTT_ClientID + ' Started')

ev3 = EV3Brick()

obstacle_sensor = InfraredSensor(Port.S4)
ev3.speaker.beep()

left_motor = Motor(Port.A)
right_motor = Motor(Port.D)


robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=160)
robot.straight(50)

'''
while True:
    
    while obstacle_sensor.distance() > 20:
        ev3.screen.print(obstacle_sensor.distance())
        robot.drive(-200, 0)
        wait(5)
    
    robot.straight(50)
    robot.turn(700)
    wait(5)
'''

