#!/usr/bin/python
# -*- coding: <encoding name> -*-

import shutil
import os
import math

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageMath

file_dir = '/tmp/pic'

class Draw(object):
    def __init__(self, size, font_size, font=None, offset=2, padding=2):
        if not isinstance(size, tuple):
            raise TypeError

        self.image = Image.new('1', size)
        self.draw = ImageDraw.Draw(self.image)
        self.width = size[0]
        self.height = size[1]
        self.max = math.floor(self.height / (font_size + padding))
        self.list = []
        self.offset = offset
        self.padding = padding
        self.font_size = font_size

        if font is not None:
            self.font = ImageFont.truetype('font.ttf', font_size)
        else:
            self.font = ImageFont.load_default()

        # For file dump
        self.file_num = 0
        try:
            shutil.rmtree(file_dir)
        except:
            pass

        os.mkdir(file_dir)

    def toggle_select(self, index):
        draw = self.draw
        offset = self.offset
        padding = self.padding
        font = self.font
        font_size = self.font_size

        box = (0, offset+1+(font_size+padding)*index, self.width-1, offset+(font_size+padding)*(index+1))
        zone = self.image.crop(box)
        # invert color
        inverted = ImageMath.eval('255-(a)', a=zone)
        self.image.paste(inverted, box=box)

    def select(self, index):
        if index > len(self.list) - 1:
            index = len(self.list) - 1

        draw = self.draw
        offset = self.offset
        padding = self.padding
        font = self.font
        font_size = self.font_size

        draw.rectangle([0, offset+1+(font_size+padding)*index, self.width-1, offset+(font_size+padding)*(index+1)], 1)
        draw.text((2, offset + (font_size + padding) * index), self.list[index], font=font, fill=0)

    def deselect(self, index):
        print(index)
        if index > len(self.list) - 1:
            index = len(self.list) - 1
        draw = self.draw
        offset = self.offset
        padding = self.padding
        font = self.font
        font_size = self.font_size

        draw.rectangle([0, offset+1+(font_size+padding)*index, self.width-1, offset+(font_size+padding)*(index+1)], 0)
        draw.text((2, offset + (font_size + padding) * index), self.list[index], font=font, fill=1)

    def reset(self):
        self.update(self.list)

    def update(self, lst):
        if self.list == lst:
            return

        self.list = lst
        draw = self.draw
        offset = self.offset
        padding = self.padding
        font = self.font
        font_size = self.font_size

        # clear all contents
        self.image.paste(0, [0, 0, self.width, self.height])

        for i in range(0, min(self.max, len(lst))):
            self.draw.text((2, offset + (font_size + padding) * i), lst[i], font=font, fill=1)

    def to_file(self):
        self.image.save(os.path.join(file_dir, str(self.file_num) + '.jpg'), 'JPEG')
        self.file_num += 1

    def to_image(self):
        return self.image

if __name__ == '__main__':
    d = Draw((128, 64), 8)
    d.to_file()

    menu = ['Get up early',
            'Goto school',
            'Rest',
            'Study',
            'Excise',
            'Sleep']

    d.update(menu)

    for i in range(6):
        d.reset()
        #  d.toggle_select(i)
        d.select(i)
        d.to_file()

    d.deselect(5)
    d.to_file()
