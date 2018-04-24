#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from subprocess import call
from app_confirm import ConfirmApp

class PoweroffApp(ConfirmApp):
    @staticmethod
    def OK(display):
        display.clear()
        display.display()

        logger = logging.getLogger('rest_request')
        logger.warning('PoweroffApp::OK, prepare to poweroff')
        call(['/usr/bin/sudo', '/sbin/poweroff'])

    def __init__(self, display, config={}):
        super(PoweroffApp, self).__init__(display, config=config)
        self.logger.debug('PoweroffApp::__init__')

        self.set_caption('Sure to poweroff?')
        self.set_callback(ok=PoweroffApp.OK, arg1=display)
        self.set_font('font.ttf')
        self.refresh()





