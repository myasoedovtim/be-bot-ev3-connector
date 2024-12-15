#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from umqtt.robust import MQTTClient
import time

#from pybricks.media.ev3dev import SoundFile, ImageFile

ev3 = EV3Brick()

MQTT_ClientID = "1fa419a0-a9fa-4866-a1e2-a0e651ec0b29"
MQTT_HOST="m6.wqtt.ru"
MQTT_PORT=17810
MQTT_USER=""
MQTT_PASSWORD=""

client = MQTTClient(MQTT_ClientID, MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASSWORD)
client.connect()

message = {
  "device_id": MQTT_ClientID,
  "name": "ev3robot",
  "description": "My first robot with bebot",
  "type": "test",
  "is_active": True,
  "actions": [],
  "sensors": []
}
def getmessages(topic, msg):
        ev3.screen.print(str(msg.decode()))

client.publish("/bebot/to/api/init", str(message))
client.set_callback(getmessages)
client.subscribe("/bebot/device/"+MQTT_ClientID)

obstacle_sensor = InfraredSensor(Port.S4)
ev3.speaker.beep()

left_motor = Motor(Port.A)
right_motor = Motor(Port.D)


robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=160)
robot.straight(50)

while True:
    client.check_msg()
    time.sleep(0.1)

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

