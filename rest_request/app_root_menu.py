#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from app_menu import MenuApp
from app_image import ImageApp
from app_umount import UmountApp
from app_about import AboutApp
from app_reboot import RebootApp
from app_poweroff import PoweroffApp
from app_excerpt_stats import StatsExcerptApp

from pi_stats_data import PiStatsData
from server_stats_data import ServerStatsData

class RootMenuApp(MenuApp):
    def __init__(self, display, devs, config):
        self.font = 'font.ttf'
        self.menu_app = [
                         ('Umount',         UmountApp),
                         ('Server Stats',   StatsExcerptApp),
                         ('Pi Stats',       StatsExcerptApp),
                         ('Show my Logo',   ImageApp),
                         ('Reboot',         RebootApp),
                         ('Poweroff',       PoweroffApp),
                         ('About',          AboutApp),
                        ]
        menu = [ i[0] for i in self.menu_app ]
        super(RootMenuApp, self).__init__(display, devs, config=config, menu=menu, font=self.font)
        self.logger.debug('RootMenuApp::__init__')

    def event_trigger(self):
        self.logger.debug('RootMenuApp::event_trigger, event = %s, app type = %s',
                          self.menu_app[self.current][0], self.menu_app[self.current][1])

        app = self.menu_app[self.current][1](self.display, self.devs, self.config)

        if self.menu_app[self.current][0] == 'Show my Logo':
            app.set('Logo2.bmp')
        elif self.menu_app[self.current][0] == 'Pi Stats':
            app.set_data_fetcher(PiStatsData)
            app.run()
        elif self.menu_app[self.current][0] == 'Server Stats':
            app.set_data_fetcher(ServerStatsData)
            app.run()


        return app


