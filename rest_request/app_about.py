#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import fcntl
import struct

from subprocess import check_output

from app import BackSchedule
from app_line_string import LineStringApp

class AboutApp(LineStringApp):
    def __init__(self, display, config):
        super(AboutApp, self).__init__(display, config)
        self.draw_image()

    def draw_image(self):
        self.set(font_size=16, box=(5, 1, 128, 20), line_height=18)

        self.redraw('About', clear=True)
        self.set('fix.ttf', font_size=8, box=(5, 23, 128-5, 32), line_height=8)
        self.redraw('Version: dev')

        self.set('fix.ttf', font_size=8, box=(5, 33, 128-5, 42), line_height=8)
        self.redraw('Author: d0u9')

        kernel = check_output(['/bin/uname', '-r']).decode('ascii').strip()
        self.set('fix.ttf', font_size=8, box=(5, 41, 128-5, 50), line_height=8)
        self.redraw('Kernel: {}'.format(kernel))

        os_name = check_output(['/bin/uname', '-s']).decode('ascii').strip()
        self.set('fix.ttf', font_size=8, box=(5, 51, 128-5, 60), line_height=8)
        self.redraw('OS: {}'.format(os_name))

        arch = check_output(['/bin/uname', '-m']).decode('ascii').strip()
        self.set('fix.ttf', font_size=8, box=(5, 61, 128-5, 70), line_height=8)
        self.redraw('Arch: {}'.format(arch))

        self.refresh()



