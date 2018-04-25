#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from math import floor
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageMath

from app import App

class MenuDraw(object):
    def __init__(self, image, font, font_size, offset, padding):
        self.logger = logging.getLogger('rest_server')
        self.logger.debug('MenuDraw::__init__')

        self.image = image
        self.offset = offset
        self.padding = padding
        self.font_size = font_size

        self.menu = []

        self.font = ImageFont.truetype(font, font_size)

        self.width = image.width
        self.height = image.height

        self.max_line = floor(self.height / (font_size + padding))
        self.draw = ImageDraw.Draw(self.image)

    def update(self, menu):
        if self.menu == menu:
            return

        self.menu = menu
        draw = self.draw
        offset = self.offset
        padding = self.padding
        font = self.font
        font_size = self.font_size

        # clear all contents
        self.image.paste(0, [0, 0, self.width, self.height])

        for i in range(0, min(self.max_line, len(menu))):
            self.draw.text((2, offset + (font_size + padding) * i), menu[i], font=font, fill=1)

    def select(self, i):
        draw = self.draw
        offset = self.offset
        padding = self.padding
        font = self.font
        font_size = self.font_size

        draw.rectangle([0, offset+1+(font_size+padding)*i, self.width-1, offset+(font_size+padding)*(i+1)], 1)
        draw.text((2, offset + (font_size + padding) * i), self.menu[i], font=font, fill=0)

    def deselect(self, i):
        draw = self.draw
        offset = self.offset
        padding = self.padding
        font = self.font
        font_size = self.font_size

        draw.rectangle([0, offset+1+(font_size+padding)*i, self.width-1, offset+(font_size+padding)*(i+1)], 0)
        draw.text((2, offset + (font_size + padding) * i), self.menu[i], font=font, fill=1)

    def reset(self):
        self.update(self.list)


class MenuApp(App):
    def __init__(self, display, devs, config, menu=[], font=None, font_size=8, offset=2, padding=2):
        if font is not None and not isinstance(font, str):
            raise TypeError

        if not isinstance(menu, list):
            raise TypeError

        if not isinstance(font_size, int) or not isinstance(offset, int) or not isinstance(padding, int):
            raise TypeError

        super(MenuApp, self).__init__(display, devs, config=config)

        self.padding = padding
        self.offset = offset
        self.font_size = font_size
        self.font = self.font if font is None else font
        self.menu = menu

        self.top_pos = 0
        self.current = 0
        self.max_line = floor(self.display.size[1] / (font_size + padding))
        self.draw = MenuDraw(self.image, self.font, self.font_size, self.offset, self.padding)

        self.draw.update(self.menu)
        self.draw.select(0)

    def event_next(self):
        self.logger.debug('MenuApp::event_next')
        if self.current == len(self.menu) - 1:
            return

        self.draw.deselect(self.current - self.top_pos)

        self.current += 1
        if self.current >= self.top_pos + self.max_line:
            self.top_pos += 1

        self.draw.update(self.menu)
        self.draw.select(self.current - self.top_pos)

        self.show()

    def event_prev(self):
        self.logger.debug('MenuApp::event_prev')
        if self.current == 0:
            return

        self.draw.deselect(self.current - self.top_pos)

        self.current -= 1
        if self.current < self.top_pos:
            self.top_pos -= 1

        self.draw.update(self.menu)
        self.draw.select(self.current - self.top_pos)

        self.show()

    def event_trigger(self):
        self.logger.debug('MenuApp::event_trigger')
        app = self.menu[self.current][1](self.display, 'Logo2.bmp')
        return app

