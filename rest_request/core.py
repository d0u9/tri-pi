#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
try:
    import RPi.GPIO as GPIO
except:
    pass

from threading import Lock
from threading import Timer

from app import App, BackSchedule

prod_lock, cust_lock = Lock(), Lock()
box = []

screen_savet_time_first = 120
screen_saver_time = 90

class Core(object):
    display = None
    config = None
    devs = None
    timer = None
    display_state = True


    @staticmethod
    def timer_cb():
        if Core.display_state is True:
            Core.display.turn_off()
            Core.devs['leds'].off_all()
            Core.display_state = False

        Core.display.screen_saver()
        Core.timer = Timer(3, Core.timer_cb)
        Core.timer.start()

    @staticmethod
    def handler_agent(event):
        logger = logging.getLogger('rest_request')
        logger.debug('Core::handler_agent, received event: %s', event)

        if Core.timer is not None:
            Core.timer.cancel()

        Core.timer = Timer(screen_saver_time, Core.timer_cb)
        Core.timer.start()

        if Core.display_state is False:
            Core.display.turn_on()
            Core.display_state = True

        if prod_lock.acquire(blocking=False):
            logger.debug('Core::handler_agent, event is queued')
            box.append(event)
            cust_lock.release()
        else:
            logger.error('Core::handler_agent, event is not queued')

    def __init__(self, display, devs, config):
        if Core.display is None:
            Core.display = display

        if Core.devs is None:
            Core.devs = devs

        if Core.config is None:
            Core.config = config

        if Core.timer is None:
            Core.timer = Timer(screen_savet_time_first, Core.timer_cb)
            Core.timer.start()

        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
        except:
            pass

        for dev in devs.values():
            dev.init()

        self.logger = logging.getLogger('rest_request')

        self.app_stack = []
        self.logger.info('Core::__ini__')

        self.prod_lock = prod_lock
        self.cust_lock = cust_lock
        self.cust_lock.acquire()
        self.box = box
        self.func_binding = {}

    def set_root_app(self, root_app):
        root = root_app(self.display, self.devs, self.config)
        self.app_stack.append(root)

    def bind_event(self, event, func):
        self.logger.info('Core::bind_event, binding %s <-> %s', event, func)

        if self.app_stack[0].make_method(func) is not None:
            self.func_binding[event] = func

    def bind_events(self, event_dict):
        if not isinstance(event_dict, dict):
            raise TypeError

        for event, callback in event_dict.items():
            self.bind_event(event, callback)

    def schedule(self):
        app = self.app_stack[-1]
        self.logger.debug('Core::schedule, to new app => %s', app)
        app.show()

    def run(self):
        if len(self.app_stack) == 0:
            raise Exception('No root app specified!')



        self.app_stack[0].show()
        while(True):
            self.logger.debug('Core::run, waiting for new event')
            self.cust_lock.acquire()
            event = box.pop(0)
            self.logger.debug('Core::run, new event arrive => %s', event)
            app = self.app_stack[-1]

            self.logger.debug('Core::run event:%s in %s', event, self.func_binding)
            if event in self.func_binding:
                func = app.make_method(self.func_binding[event])
                ret = func()
                if isinstance(ret, App):
                        self.app_stack.append(ret)
                        self.schedule()
                if isinstance(ret, BackSchedule):
                        self.app_stack.pop()
                        self.schedule()
            else:
                self.logger.error('Core::run, event %s not hit', event)

            self.prod_lock.release()
