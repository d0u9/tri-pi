#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from PIL import Image

from display import Display

class BackSchedule(object):
    pass

class App(object):
    def __init__(self, display, devs, config):
        self.logger = logging.getLogger('rest_request')

        if not isinstance(display, Display):
            raise TypeError

        self.display = display
        self.font = 'font.ttf'
        self.image = Image.new('1', self.display.size)
        self.config = config
        self.devs = devs

    def event_next(self):
        self.logger.warning('App::event_next - default next event handler')

    def event_prev(self):
        self.logger.warning('App::event_prev - default prev event handler')

    def event_trigger(self):
        self.logger.warning('App::event_trigger - default trigger event handler')

    def event_back(self):
        self.logger.warning('App::event_back - default back event handler')

    def show(self):
        self.logger.debug('App::show')
        self.display.refresh(self.image)

    def make_method(self, name):
        if   name == 'event_next':
            return self.event_next
        elif name == 'event_prev':
            return self.event_prev
        elif name == 'event_trigger':
            return self.event_trigger
        elif name == 'event_back':
            return self.event_back
        else:
            return None


