#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import signal

from time import sleep
from core import Core

class Button(object):
    def __init__(self):
        self.logger = logging.getLogger('rest_request')

    @staticmethod
    def handler_cb():
        pass

    def get_binding(self):
        return []

try:
    import RPi.GPIO as GPIO

    class PhyButton(Button):
        def __init__(self):
            super(PhyButton, self).__init__()

            self.btn_prev = 6
            self.btn_down = 13
            self.btn_trigger = 19
            self.btn_back = 26

            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup([self.btn_prev, self.btn_down, self.btn_trigger, self.btn_back], GPIO.IN, pull_up_down=GPIO.PUD_OFF)
            GPIO.add_event_detect(self.btn_prev,    GPIO.FALLING, PhyButton.handler_cb)
            GPIO.add_event_detect(self.btn_down,    GPIO.FALLING, PhyButton.handler_cb)
            GPIO.add_event_detect(self.btn_trigger, GPIO.FALLING, PhyButton.handler_cb)
            GPIO.add_event_detect(self.btn_back,    GPIO.FALLING, PhyButton.handler_cb)

        @staticmethod
        def handler_cb(pin):
            logger = logging.getLogger('rest_request')
            logger.debug('PhyButton: register handler callback')
            sleep(0.01)
            if GPIO.input(pin) is not 0:
                logger.debug('PhyButton: Mis-pressed buttong')
                return

            Core.handler_agent(pin)

        def get_binding(self):
            binding = { self.btn_prev:     'event_prev',
                        self.btn_down:     'event_next',
                        self.btn_trigger:  'event_trigger',
                        self.btn_back:     'event_back' }
            self.logger.debug('PhyButtong: binding -> %s', binding)

            return binding
except:
    pass

class VirButton(Button):
    def __init__(self):
        super(VirButton, self).__init__()

        signal.signal(signal.SIGUSR1, VirButton.handler_cb)
        signal.signal(signal.SIGUSR2, VirButton.handler_cb)
        signal.signal(signal.SIGALRM, VirButton.handler_cb)
        signal.signal(signal.SIGCONT, VirButton.handler_cb)

    @staticmethod
    def handler_cb(signal, frame):
        logger = logging.getLogger('rest_request')
        logger.debug('VirButton: register handler callback')
        Core.handler_agent(signal)

    def get_binding(self):
        binding = {signal.SIGUSR1: 'event_prev',
                   signal.SIGUSR2: 'event_next',
                   signal.SIGALRM: 'event_trigger',
                   signal.SIGCONT: 'event_back'}
        self.logger.debug('VirButtong: binding -> %s', binding)

        return binding

