#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from subprocess import call
from app_confirm import ConfirmApp

class RebootApp(ConfirmApp):
    @staticmethod
    def OK(display):
        display.clear()
        display.display()

        logger = logging.getLogger('rest_request')
        logger.warning('PoweroffApp::OK, prepare to reboot')
        call(['/usr/bin/sudo', '/sbin/reboot'])

    def __init__(self, display, devs, config={}):
        super(RebootApp, self).__init__(display, devs, config=config)
        self.logger.debug('RebootApp::__init__')

        self.set_caption('Sure to reboot?')
        self.set_callback(ok=RebootApp.OK, arg1=display)
        self.set_font('font.ttf')
        self.refresh()





