#!/usr/bin/python3
import RPi.GPIO as GPIO

class TurnSense:
    leftSensor = 14
    rightSensor = 15

    rightActive = 0
    leftActive = 0

    def init_GPIO(self):
        print("TurnSense: Initializing IO...")
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.leftSensor, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.setup(self.rightSensor, GPIO.IN, GPIO.PUD_DOWN)
        print("TurnSense: IO Initialized")

    def left_engaged(channel):
        if GPIO.input(channel):
            GearSense.leftActive = 1
        else:
            GearSense.leftActive = 0
        return True

    def right_engaged(channel):
        if GPIO.input(channel):
            GearSense.rightActive = 1
        else:
            GearSense.rightActive = 0
        return True

    def init_interrupt(self):
        print('TurnSense: Setting GPIO events...')
        GPIO.add_event_detect(self.leftSensor, GPIO.RISING, callback=self.left_engaged, bouncetime=20)
        GPIO.add_event_detect(self.rightSensor, GPIO.RISING, callback=self.right_engaged, bouncetime=20)
        print('TurnSense: GPIO events set.')