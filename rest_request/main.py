#!/usr/bin/python
# -*- coding: <encoding name> -*-

import time
import logging

from logging.handlers import RotatingFileHandler

from PIL import Image

from oled import Oled
from draw import Draw
from display import Display
from menu import Menu, Item

log_formatter = logging.Formatter('[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S %z')

log_file = '/run/rest_request/rest_server.log'
file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024)
file_handler.setFormatter(log_formatter)

stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(log_formatter)

logger = logging.getLogger('rest_request')
logger.addHandler(file_handler)
logger.addHandler(stdout_handler)
logger.setLevel(logging.INFO)

def cb_show_version(version):
    print('version: ', version)

def cb_umount_disk(args):
    print('umount')

class Tri(object):
    def __init__(self):
        self.max_line_num = 6
        self.oled = Oled()
        self.init_menu()
        self.display = Display(self.menu, self.max_line_num)
        self.draw = Draw(self.oled.size(), font_size=8)

    def init_menu(self):
        m_root = Menu('root')
        m_root.add(('Umount Disk', cb_umount_disk, ''))
        m_root.add(('Show Version', cb_show_version, '1.1'))
        m_root.add(('a1', cb_show_version, 'a1'))
        m_root.add(('a2', cb_show_version, 'a2'))
        m_root.add(('a3', cb_show_version, 'a3'))
        m_root.add(('a4', cb_show_version, 'a4'))
        m_root.add(('a5', cb_show_version, 'a5'))
        m_root.add(('a6', cb_show_version, 'a6'))
        self.menu = m_root

    def run(self):
        image = Image.open('Logo2.bmp').convert('1')
        self.oled.refresh(image)
            
        time.sleep(1)

        for i in range(0, 10):
            self.oled.refresh(self.draw.to_image())
            self.draw.update(self.display.captions())
            self.draw.select(self.display.cursor())
            self.oled.refresh(self.draw.to_image())
            self.display.triger()
            time.sleep(1)
            self.draw.deselect(self.display.cursor())
            self.display.next()

        print('-----')
        time.sleep(1)

        for i in range(0, 10):
            self.oled.refresh(self.draw.to_image())
            self.draw.update(self.display.captions())
            self.draw.select(self.display.cursor())
            self.oled.refresh(self.draw.to_image())
            time.sleep(1)
            self.draw.deselect(self.display.cursor())
            self.display.prev()


if __name__ == '__main__':
    logger.info('Starting...')

    t = Tri()
    t.run()

    

