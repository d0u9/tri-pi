#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from threading import Lock

from app import App, BackSchedule

prod_lock, cust_lock = Lock(), Lock()
box = []

class Core(object):
    @staticmethod
    def handler_agent(event):
        logger = logging.getLogger('rest_request')
        logger.debug('Core::handler_agent, received event: %s', event)

        if prod_lock.acquire(blocking=False):
            logger.debug('Core::handler_agent, event is queued')
            box.append(event)
            cust_lock.release()
        else:
            logger.error('Core::handler_agent, event is not queued')

    def __init__(self, root_app):
        self.logger = logging.getLogger('rest_request')

        self.app_stack = [root_app,]
        self.logger.info('Core::__ini__, root app is %s', root_app)

        self.prod_lock = prod_lock
        self.cust_lock = cust_lock
        self.cust_lock.acquire()
        self.box = box
        self.func_binding = {}

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
