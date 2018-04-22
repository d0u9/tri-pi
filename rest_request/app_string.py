#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import floor
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageMath

from app import App, BackSchedule
from time import sleep

class StringDraw(object):
    def __init__(self, image, font):
        self.image = image
        self.font_name = font
        self.x, self.y = (0, 0)

        self.width = image.width
        self.height = image.height
        self.draw = ImageDraw.Draw(self.image)

    def clear(self):
        self.draw.rectangle([0, 0, self.width-1, self.height-1], fill=0)

    def redraw(self, string, font=None, font_size=None, pos=None, clear=False):
        if clear:
            self.clear()
        self.font_name = self.font_name if font is None else font
        self.font_size = self.font_size if font_size is None else font_size
        self.x, self.y = (self.x, self.y) if pos is None else pos
        f = ImageFont.truetype(self.font_name, self.font_size)
        self.draw.text((self.x, self.y), string, font=f, fill=1)

class StringApp(App):
    def __init__(self, display, config={}):
        super(StringApp, self).__init__(display, config=config)
        self.font_name = self.font
        self.pos = (0, 0)
        self.str = ''
        self.font_size = 8

        self.draw = StringDraw(self.image, self.font)

    def event_next(self):
        self.logger.debug('StringApp::event_next')

    def event_prev(self):
        self.logger.debug('StringApp::event_prev')

    def event_trigger(self):
        self.logger.debug('StringApp::event_trigger')
        return BackSchedule()

    def event_back(self):
        self.logger.debug('StringApp::event_back')
        return BackSchedule()

    def redraw(self, string, clear=False):
        self.str = string
        self.draw.redraw(string, self.font_name, self.font_size, self.pos, clear)

    def set(self, font=None, font_size=None, pos=None):
        self.font_name = self.font_name if font is None else font
        self.pos = self.pos if pos is None else pos
        self.font_size = self.font_size if font_size is None else font_size

