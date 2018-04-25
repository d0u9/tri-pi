#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO

from device import Device

class LedDev(Device):
    RED = 16
    GREEN = 20
    BLUE = 21

    level_dict = { True: GPIO.HIGH, False: GPIO.LOW }
    state = { RED: False, GREEN: False, BLUE: False }

    @staticmethod
    def init():
        Device.init()
        GPIO.setup([LedDev.RED, LedDev.GREEN, LedDev.BLUE], GPIO.OUT, initial=GPIO.LOW)

    def on(led):
        if led not in [LedDev.RED, LedDev.GREEN, LedDev.BLUE]:
            return

        state = True
        LedDev.state[led] = state
        GPIO.output(led, LedDev.level_dict[state])

    @staticmethod
    def off(led):
        if led not in [LedDev.RED, LedDev.GREEN, LedDev.BLUE]:
            return

        state = False
        LedDev.state[led] = state
        GPIO.output(led, LedDev.level_dict[state])

    @staticmethod
    def toggle(led):
        if led not in [LedDev.RED, LedDev.GREEN, LedDev.BLUE]:
            return

        state = not LedDev.state[led]
        LedDev.state[led] = state
        GPIO.output(led, LedDev.level_dict[state])

    def off_all():
        for led in [LedDev.RED, LedDev.GREEN, LedDev.BLUE]:
            LedDev.off(led)

    def on_all():
        for led in [LedDev.RED, LedDev.GREEN, LedDev.BLUE]:
            LedDev.on(led)


