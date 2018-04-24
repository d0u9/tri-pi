#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import fcntl
import struct

from subprocess import check_output

from app import BackSchedule
from app_string import StringApp

class AboutApp(StringApp):
    def __init__(self, display, config):
        super(AboutApp, self).__init__(display, config)
        self.draw_image()

    def draw_image(self):
        self.set(font_size=16, pos=(5, 1))
        self.redraw('About', clear=True)

        self.set(font_size=8, pos=(5, 22))
        self.redraw('Version: dev')

        self.set(font_size=8, pos=(5, 32))
        self.redraw('Author: d0u9')

        kernel = check_output(['/bin/uname', '-r']).decode('ascii').strip()
        self.set(font_size=8, pos=(5, 42))
        self.redraw('Kernel: {}'.format(kernel))

        os_name = check_output(['/bin/uname', '-s']).decode('ascii').strip()
        arch = check_output(['/bin/uname', '-m']).decode('ascii').strip()
        self.set(font_size=8, pos=(5, 52))
        self.redraw('{} on {}'.format(os_name, arch))

        self.refresh()



