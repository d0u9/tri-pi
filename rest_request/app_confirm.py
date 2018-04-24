#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageMath

from app import BackSchedule
from app_line_string import LineStringApp

class ConfirmApp(LineStringApp):
    def __init__(self, display, config={}):
        super(ConfirmApp, self).__init__(display, config=config)

        self.ok = None
        self.cancle = None
        self.caption = '\n'
        self.arg1 = None
        self.arg2 = None

    def set_caption(self, caption='\n'):
        self.caption = caption

    def set_callback(self, ok=None, arg1=None, cancle=None, arg2=None):
        self.ok = self.ok if ok is None else ok
        self.arg1 = self.arg1 if arg1 is None else arg1
        self.cancle = self.cancle if cancle is None else cancle
        self.arg2 = self.arg2 if arg2 is None else arg2

    def set_font(self, font='fix.ttf', font_size=8, line_height=10):
        self.font_name = font
        self.font_size = font_size
        self.line_height = line_height

    def event_trigger(self):
        if self.ok is not None:
            self.ok(self.arg1)
        return BackSchedule()

    def event_back(self):
        if self.cancle is not None:
            self.cancle(self.arg2)
        return BackSchedule()

    def refresh(self):
        self.set(font=self.font_name, font_size=self.font_size, box=(5,5,122,58), line_height=self.line_height)
        self.redraw(self.caption, clear=True)
        super(ConfirmApp, self).refresh()


