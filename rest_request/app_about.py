#!/usr/bin/python
# -*- coding: utf-8 -*-

from app import BackSchedule
from app_string import StringApp

class AboutApp(StringApp):
    def __init__(self, display, config):
        super(AboutApp, self).__init__(display, config)

        self.set(font_size=16, pos=(0,0))
        self.redraw('Hello Wrold!!!', clear=True)
        self.set(pos=(0, 32))
        self.redraw('Version: dev')
