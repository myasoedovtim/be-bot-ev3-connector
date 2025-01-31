#!/usr/bin/env pybricks-micropython
# Подключение библиотек.
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from umqtt.robust import MQTTClient
import time
import json
from pybricks.media.ev3dev import SoundFile, ImageFile

# Создание объекта класса EV3Brick (модуль ev3).
ev3 = EV3Brick()

# Заполнение переменных параметрами подключения к брокеру mqtt.
# Идентификатор устройства (использовался генератор https://www.uuidgenerator.net/guid).
MQTT_ClientID = "1fa419a0-a9fa-4866-a1e2-a0e651ec0b29"
# Хост брокера (IP адрес или доменное имя).
MQTT_HOST="m6.wqtt.ru"
# Порт брокера.
MQTT_PORT=17810
# Имя пользователя.
MQTT_USER=""
# Пароль.
MQTT_PASSWORD=""

# Создание объекта класса MQTTClient (передаем параметры подключения).
client = MQTTClient(MQTT_ClientID, MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASSWORD)
# Подключение к брокеру mqtt.
client.connect()

# Сообщение для инициализации (добавления) устройства в bebot.api.
message = {
  "device_id": MQTT_ClientID,
  "name": "ev3robot",
  "description": "My first robot with bebot",
  "type": "test",
  "is_active": True,
  "actions": ["forward","backward", "left", "right"],
  "sensors": ["Infrared"]
}

# Функция обработки входящих сообщений.
def getmessages(topic, msg):
     # Сообщение на экран ev3 с текстом полученного сообщения (для отладки).
     ev3.screen.print(str(msg.decode()))
     # Преобразование в формат JSON.
     data = json.loads(msg.decode())
     # Проверяем наличие ключа forward в полученном сообщении.
     if "forward" in data:
          # Подаем команду на двигатели (отрицательное значение, потому что моторы стоят наоборот).
          robot.straight(-data["backward"])
     # Проверяем наличие ключа forward в полученном сообщении
     if "backward" in data:
          # Подаем команду на двигатели.
          robot.straight(data["backward"])
     # Проверяем наличие ключа left в полученном сообщении
     if "left" in data:
          # Подаем команду на двигатели.
          left_motor.dc(data["left"])
     # Проверяем наличие ключа right в полученном сообщении
     if "right" in data:
          # Подаем команду на двигатели.
          left_motor.dc(data["left"])
     # Проверяем наличие ключа getsensor в полученном сообщении
     if "getsensor" in data:
          # Проверяем, что запрошены данные инфрокрасного датчика.
          if data["getsensor"] == "Infrared":
               # Отображаем данные сенсора на экране (для отладки).
               ev3.screen.print(obstacle_sensor.distance())
               # Формируем json сообщение с данными сенсора для отправки.
               sensor_message = {"device_id": MQTT_ClientID,"name": "Infrared","value": obstacle_sensor.distance()}
               # Публикуем сообщение в брокере.
               client.publish("/bebot/to/api/sensor", str(sensor_message))


# Публикация сообщения инициализации.
client.publish("/bebot/to/api/init", str(message))
# Установка функции обработчика входящих сообщений.
client.set_callback(getmessages)
# Подписываемся на очередь bebot/device/идентификатор_текущего_устройства.
client.subscribe("/bebot/device/"+MQTT_ClientID)

# Инициализируем инфрокрасный датчик.
obstacle_sensor = InfraredSensor(Port.S4)
# Инициализируем левый мотор.
left_motor = Motor(Port.A)
# Инициализируем правый мотор.
right_motor = Motor(Port.D)
# Инициализируем общее управление двигателями (с учетом диаметра колес и расстояния между ними).
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=160)

# Подаем звуковой сигнал об успешной загрузке управляющей программы.
ev3.speaker.beep()

#Отображаем на дисплее текущий заряд батареи
ev3.screen.print("Voltage is: {}".format(brick.battery.voltage()))

# Счетчик циклов (используется для отправки сообщений со статусом робота).
counter = 0
# Бесконечный цикл ожидания входящих сообщений (команд).
while True:
    # Инкремент счетчика.
    counter+=1
    # Проверка наличия входящих сообщений в очередях (на которые подписались).
    client.check_msg()
    # Прерывание цикла на 1/100 секунды (иначе процессор будет загружен только проверкой сообщений).
    time.sleep(0.01)
    # Каждый 1000 цикл отправляем сообщение со статусом (устройство активно).
    if counter%1000 == 0:
        # Сообщение на экран ev3.
        ev3.screen.print("Time to send status...")
        # Отправка инициализационного сообщения (в нем установлен статус "is_active": True).
        client.publish("/bebot/to/api/status", str(message))

