#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from app_menu import MenuApp
from app_image import ImageApp
from app_umount import UmountApp
from app_about import AboutApp

class RootMenuApp(MenuApp):
    def __init__(self, display, config):
        self.font = 'font.ttf'
        self.menu_app = [
                         ('Umount',         UmountApp),
                         ('Show my Logo',   ImageApp),
                         ('About',          AboutApp)
                        ]
        menu = [ i[0] for i in self.menu_app ]
        super(RootMenuApp, self).__init__(display, config=config, menu=menu, font=self.font)
        self.logger.debug('RootMenuApp::__init__')

    def event_trigger(self):
        self.logger.debug('RootMenuApp::event_trigger, event = %s, app type = %s',
                          self.menu_app[self.current][0], self.menu_app[self.current][1])

        app = self.menu_app[self.current][1](self.display, self.config)

        if self.menu_app[self.current][0] == 'Show my Logo':
            app.set('Logo2.bmp')

        return app

