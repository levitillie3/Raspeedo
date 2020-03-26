#!/usr/bin/python3

#https://lb.raspberrypi.org/forums/viewtopic.php?t=151465
import RPi.GPIO as GPIO
from datetime import *
from time import sleep
import time, math

class SensorReadout:
    #process params
    dist_meas = 0.00
    olddist_meas = 0.00   # last loop
    mi_per_hour = 0
    mph = 0
    rpm = 0
    elapse = 0
    pulse = 0

    #your params to set:
    sleeptime = .1        # secs between reporting loop
    secsnoread = .05      # number of seconds rotor is stationary before a 'no read' is declared and set result to zero - depends on inertia of your rotor in light >no wind
    errortime = 90        # number of seconds of no activity before error/stationary warning is shown - set high after debugging
    loopcount = 0         # a 'nothing is happening' counter
    r_cm = 22            # cm wheel radius as parameter (assumed centre of cups)
    sensor = 2          # BCM
    magnets = 3           # how many magnets in your rotor? (code assumes one sensor though)

    #startup numbers
    circ_cm = 2*math.pi*r_cm            # calculate wheel circumference in CM (1 rotation)
    dist_mi = circ_cm/160934/magnets    # convert cm to mi (rotation/magnets)
    start_timer = time.time()           # for interrupt function

    def init_GPIO(self):			    # initialize GPIO
        print('SpeedSense: Initializing IO...')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.sensor,GPIO.IN,GPIO.PUD_UP)
        print('SpeedSense: IO Initialized')

    def calculate_elapse(channel):          # callback function
        SensorReadout.pulse += 1			                # increase pulse by 1 whenever interrupt occurred
        SensorReadout.elapse = time.time() - SensorReadout.start_timer  # elapsed time for a half rotation causing a pulse (edit for hall sensor 2 magnets)
        SensorReadout.start_timer = time.time()		    # let current time equals to start_timer

    def calculate_speed(self):
        try:
            self.rpm = 1/self.elapse * 60/self.magnets     # 2 interrupts per rotation made
            self.mph= self.dist_mi / self.elapse * 3600    # calculate mi/hour
            self.dist_meas = self.dist_mi*self.pulse       # measure distance traverse in mi
            if self.dist_meas == self.olddist_meas:
                self.mph = 0
                self.rpm = 0
            return self.mph
        except ZeroDivisionError:
            pass

    def report(self, mode):
            if mode == 'realtime':                  # comment this mode if you want a quieter report, or use
                return '{0:.1f} Mph'.format(self.mph)
            elif mode == 'error':
                return '0 Mph'
            else:
                print('bad report mode')

    def init_interrupt(self):
        print('SpeedSense: Setting GPIO events...')
        GPIO.add_event_detect(self.sensor, GPIO.FALLING, callback = self.calculate_elapse, bouncetime = 20)
        print('SpeedSense: GPIO events set.')

    def start_read(self):
        self.init_GPIO(self)
        self.init_interrupt(self)
        self.calculate_speed(self)
        while True:
            self.olddist_meas = self.dist_meas
            self.calculate_speed(self)
            if self.olddist_meas != self.dist_meas:
                self.loopcount = 0
                return self.report(self, 'realtime')
            else:
                self.loopcount += 1
                if self.loopcount == self.secsnoread/self.sleeptime:     # its stopped, force show a zero as it might be 'between magnets' and show last value
                    return self.report('realtime')
                if self.loopcount == 20/self.sleeptime:
                    self.loopcount = self.secsnoread/self.sleeptime + 1
                    self.report(self, "error")