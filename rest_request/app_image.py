#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageMath

from app import App, BackSchedule

class ImageApp(App):
    def __init__(self, display, devs, config={}):
        super(ImageApp, self).__init__(display, devs, config=config)
        self.pic = None
        self.image = None

    def event_next(self):
        self.logger.debug('ImageApp::event_next')

    def event_prev(self):
        self.logger.debug('ImageApp::event_prev')

    def event_trigger(self):
        self.logger.debug('ImageApp::event_trigger')

    def event_trigger(self):
        self.logger.debug('ImageApp::event_trigger')
        return BackSchedule()

    def event_back(self):
        self.logger.debug('ImageApp::event_back')
        return BackSchedule()

    def set(self, pic):
        self.pic = pic

    def show(self):
        self.image = Image.open(self.pic).convert('1')
        self.image.thumbnail(self.display.size, Image.ANTIALIAS)
        self.display.refresh(self.image)

