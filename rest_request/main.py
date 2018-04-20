#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler
from time import sleep

from core import Core
from btn import VirButton
from app import App
from display import DisplayFile
from app_image import ImageApp
from app_root_menu import RootMenuApp

from app_image import ImageApp


log_formatter = logging.Formatter('[%(asctime)s] [%(process)d] [%(levelname)s]->[%(filename)s:%(lineno)d] %(message)s', '%Y-%m-%d %H:%M:%S %z')

try:
    from btn import PhyButton
    from display import DisplayOled
    log_file = '/run/rest_request/rest_server.log'
except:
    log_file = '/tmp/rest_server.log'

file_handler = RotatingFileHandler(log_file, mode=664, maxBytes=5 * 1024 * 1024)
file_handler.setFormatter(log_formatter)

stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(log_formatter)

logger = logging.getLogger('rest_request')
logger.addHandler(file_handler)
logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    logger.info('start...')
    logger.debug('Debug Mode')

    try:
        btn = PhyButton()
    except:
        btn = VirButton()

    key_binding = btn.get_binding()

    try:
        display = DisplayOled()
    except:
        display = DisplayFile('/tmp/to_file')

    root = RootMenuApp(display)

    core = Core(root)
    core.bind_events(key_binding)

    start_up = ImageApp(display)
    start_up.set('Logo2.bmp')
    start_up.show()
    sleep(1)

    core.run()

