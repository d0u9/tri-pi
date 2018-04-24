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
        self.font = 'font.ttf'

    def draw_image(self):
        self.set(font_size=16, box=(5, 1, 128, 20), line_height=18)

        self.redraw('About', clear=True)
        self.set(self.font, font_size=8, box=(5, 23, 128-5, 32), line_height=10)
        self.redraw('Version: dev')

        self.set(self.font, font_size=8, box=(5, 33, 128-5, 42), line_height=10)
        self.redraw('Author: d0u9')

        kernel = check_output(['/bin/uname', '-r']).decode('ascii').strip()
        self.set(self.font, font_size=8, box=(5, 43, 128-5, 52), line_height=10)
        self.redraw('Kernel: {}'.format(kernel))

        os_name = check_output(['/bin/uname', '-s']).decode('ascii').strip()
        self.set(self.font, font_size=8, box=(5, 53, 128-5, 62), line_height=10)
        self.redraw('OS: {}'.format(os_name))

        arch = check_output(['/bin/uname', '-m']).decode('ascii').strip()
        self.set(self.font, font_size=8, box=(5, 63, 128-5, 72), line_height=10)
        self.redraw('Arch: {}'.format(arch))

        self.refresh()



