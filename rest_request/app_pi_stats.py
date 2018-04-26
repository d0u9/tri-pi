#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from threading import Timer

from app_line_string import LineStringApp

class PiStatsApp(LineStringApp):
    def __init__(self, display, devs, config={}):
        super(PiStatsApp, self).__init__(display, devs, config)
        self.set(font_size=16, box=(5,5, 122, 58), line_height=18)
        self.i = 0
        self.draw_image()
        t = Timer(2, self.timer_cb)
        t.start()

    def draw_image(self):
        self.redraw('Pi Stats: {}'.format(self.i))
        self.i += 1

        self.refresh()

    def timer_cb(self):
        self.draw_image()
        self.show()
        t = Timer(2, self.timer_cb)
        t.start()

