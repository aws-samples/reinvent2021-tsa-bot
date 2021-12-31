
import serial
import time
import os
import psutil
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
import os
import RPi.GPIO as GPIO
kit = ServoKit(channels=16)

def initialAvaIntroServo():
    # AVA moving head
    kit.servo[10].angle = 120
    time.sleep(3)
    kit.servo[10].angle = 90
    time.sleep(3)
    kit.servo[10].angle = 60
    time.sleep(3)
    kit.servo[10].angle = 90
    time.sleep(3)

initialAvaIntroServo()