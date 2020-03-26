#!/usr/bin/python3
import RPi.GPIO as GPIO

class GearSense:

    neutralSensor = 4
    firstSensor = 17
    secondSensor = 27
    thirdSensor = 22
    fourthSensor = 10
    fifthSensor = 9
    ODSensor = 11

    neutralActive = 0
    firstActive = 0
    secondActive = 0
    thirdActive = 0
    fourthActive = 0
    fifthActive = 0
    ODActive = 0

    def init_GPIO(self):
        print('GearSense: Initializing IO...')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.neutralSensor, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.setup(self.firstSensor, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.setup(self.secondSensor, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.setup(self.thirdSensor, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.setup(self.fourthSensor, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.setup(self.fifthSensor, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.setup(self.ODSensor, GPIO.IN, GPIO.PUD_DOWN)
        print('GearSense: IO Initialized')

    def neutral_engaged(channel):
        if GPIO.input(channel):
            GearSense.neutralActive = 1
        else:
            GearSense.neutralActive = 0
        return True

    def first_engaged(channel):
        if GPIO.input(channel):
            GearSense.firstActive = 1
        else:
            GearSense.firstActive = 0
        return True

    def second_engaged(channel):
        if GPIO.input(channel):
            GearSense.secondActive = 1
        else:
            GearSense.secondActive = 0
        return True

    def third_engaged(channel):
        if GPIO.input(channel):
            GearSense.thirdActive = 1
        else:
            GearSense.thirdActive = 0
        return True

    def fourth_engaged(channel):
        if GPIO.input(channel):
            GearSense.fourthActive = 1
        else:
            GearSense.fourthActive = 0
        return True

    def fifth_engaged(channel):
        if GPIO.input(channel):
            GearSense.fifthActive = 1
        else:
            GearSense.fifthActive = 0
        return True

    def OD_engaged(channel):
        if GPIO.input(channel):
            GearSense.ODActive = 1
        else:
            GearSense.ODActive = 0
        return True

    def init_interrupt(self):
        print('GearSense: Setting GPIO events...')
        GPIO.add_event_detect(self.neutralSensor, GPIO.RISING, callback=self.neutral_engaged, bouncetime=20)
        GPIO.add_event_detect(self.firstSensor, GPIO.RISING, callback=self.first_engaged, bouncetime=20)
        GPIO.add_event_detect(self.secondSensor, GPIO.RISING, callback=self.second_engaged, bouncetime=20)
        GPIO.add_event_detect(self.thirdSensor, GPIO.RISING, callback=self.third_engaged, bouncetime=20)
        GPIO.add_event_detect(self.fourthSensor, GPIO.RISING, callback=self.fourth_engaged, bouncetime=20)
        GPIO.add_event_detect(self.fifthSensor, GPIO.RISING, callback=self.fifth_engaged, bouncetime=20)
        GPIO.add_event_detect(self.ODSensor, GPIO.RISING, callback=self.OD_engaged, bouncetime=20)
        print('GearSense: GPIO events set.')