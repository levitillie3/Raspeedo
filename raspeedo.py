#!/usr/bin/python3
from readspeedsensor import SensorReadout
from gearsensor import GearSense
from turnsignalsensor import TurnSense
from signal import signal, SIGINT
import gi
import time
import RPi.GPIO as GPIO
gi.require_version('Gtk', '3.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, GLib, Pango, GdkPixbuf


class RaspeedoUI:

    def __init__(self):
        self.gladefile = "raspeedo.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(Handler())
        self.window = self.builder.get_object("Raspeedo")
        self.Clock = self.builder.get_object("lbl_time")
        self.Speed = self.builder.get_object("lbl_speed")
        self.Speed.set_label('0 Mph')
        SpeedAttrs = Pango.FontDescription('normal 47')
        self.Speed.override_font(SpeedAttrs)
        self.window.show()

    def displayclock(self):
        t = time.localtime()
        datetimenow = time.strftime("%a %b %d %H:%M%p", t)
        self.Clock.set_label(datetimenow)
        ClockAttrs = Pango.FontDescription('normal 35')
        self.Clock.override_font(ClockAttrs)
        return True

    def convertTuple(self, tup):
        str = ''.join(tup)
        return str

    def displayspeed(self):
        sr = SensorReadout
        sr.olddist_meas = sr.dist_meas
        sr.calculate_speed(sr)
        if sr.olddist_meas != sr.dist_meas:
            if int(sr.mph) >= 1:
                sr.loopcount = 0
                speedtup = sr.report(sr, "realtime")
                speed_str = self.convertTuple(speedtup)
                self.Speed.set_label(speed_str)
            else:
                self.Speed.set_label('0 Mph')
            return True
        else:
            sr.loopcount += 1
            if sr.loopcount == sr.secsnoread/sr.sleeptime:
                speedtup = sr.report(sr, "realtime")
                speed_str = self.convertTuple(speedtup)
                self.Speed.set_label(speed_str)
            if sr.loopcount == 20/sr.sleeptime:
                sr.loopcount = sr.secsnoread/sr.sleeptime+1
                self.Speed.set_label('0 Mph')
            return True

    def displaygear(self):
        self.Neutral = self.builder.get_object("neutral_ind")
        self.Gear = self.builder.get_object("lbl_gear")
        GearAttrs = Pango.FontDescription('normal 70')
        self.Gear.override_font(GearAttrs)
        if GearSense.neutralActive == 1:
            self.Gear.hide()
            self.Neutral.show()
        elif GearSense.neutralActive == 0:
            self.Gear.show()
            self.Neutral.hide()
        elif GearSense.firstActive == 1:
            self.Neutral.hide()
            self.Gear.set_label('1')
        elif GearSense.firstActive == 0:
            self.Neutral.hide()
        elif GearSense.secondActive == 1:
            self.Neutral.hide()
            self.Gear.set_label('2')
        elif GearSense.secondActive == 0:
            self.Neutral.hide()
        elif GearSense.thirdActive == 1:
            self.Neutral.hide()
            self.Gear.set_label('3')
        elif GearSense.thirdActive == 0:
            self.Neutral.hide()
        elif GearSense.fourthActive == 1:
            self.Neutral.hide()
            self.Gear.set_label('4')
        elif GearSense.fourthActive == 0:
            self.Neutral.hide()
        elif GearSense.fifthActive == 1:
            self.Neutral.hide()
            self.Gear.set_label('5')
        elif GearSense.fifthActive == 0:
            self.Neutral.hide()
        elif GearSense.ODActive == 1:
            self.Neutral.hide()
            self.Gear.set_label('O.D.')
        elif GearSense.ODActive == 0:
            self.Neutral.hide()
        return True

    def displayTurnIndicator(self):
        leftanim = GdkPixbuf.PixbufAnimation.new_from_file("leftarrowsmall.gif")
        rightanim = GdkPixbuf.PixbufAnimation.new_from_file("rightarrowsmall.gif")
        self.left = self.builder.get_object("left_ind")
        self.right = self.builder.get_object("right_ind")
        self.left.set_from_animation(leftanim)
        self.right.set_from_animation(rightanim)
        #self.left.show()
        #self.right.show()
        if TurnSense.leftActive == 1:
            self.left.show()
        if TurnSense.leftActive == 0:
            self.left.hide()
        if TurnSense.rightActive == 1:
            self.right.show()
        if TurnSense.rightActive == 0:
            self.right.hide()
        return True

    def startClockLoop(self):
        print('starting Clock')
        GLib.timeout_add(100, self.displayclock)

    def startSpeedLoop(self):
        print('starting Speedo')
        GLib.timeout_add(100, self.displayspeed)

    def startGearLoop(self):
        print('starting Gears')
        GLib.timeout_add(10, self.displaygear)

    def startTurnSignalLoop(self):
        print('starting Turn Signals')
        GLib.timeout_add(1000, self.displayTurnIndicator)

    def startMonLoops(self):
        self.startClockLoop()
        self.startSpeedLoop()
        self.startGearLoop()
        self.startTurnSignalLoop()

class Handler:

    def onDestroy(self, *args):
        GPIO.cleanup()
        Gtk.main_quit()

def init_GPIO():
    SensorReadout.init_GPIO(SensorReadout)
    SensorReadout.init_interrupt(SensorReadout)
    GearSense.init_GPIO(GearSense)
    GearSense.init_interrupt(GearSense)
    TurnSense.init_GPIO(TurnSense)
    TurnSense.init_interrupt(TurnSense)

def exiter(signal_recieved, frame):
    GPIO.cleanup()
    Gtk.main_quit()

if __name__ == "__main__":
    signal(SIGINT, exiter)
    init_GPIO()
    main = RaspeedoUI()
    main.startMonLoops()
    Gtk.main()