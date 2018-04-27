#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageMath

class TextDraw(object):
    def __init__(self, image):
        self.image = image
        self.d = ImageDraw.Draw(self.image)

        self.font_name = 'font.ttf'
        self.font_size = 8
        self.font = ImageFont.truetype(self.font_name, self.font_size)

    def set_font(font_name='font.ttf', font_size=8):
        self.font_name = font_name
        self.font_size = font_size
        self.font = ImageFont.truetype(self.font_name, self.font_size)

    def size(self, text):
        return self.d.textsize(text, font=self.font)

    def draw(self, text, box, align='left'):
        pos = (box[0], box[1])

        if align == 'right':
            pos = (box[2] - self.size(text)[0], box[1])
        elif align == 'center':
            x = (box[0] + box[2] - self.size(text)[0]) / 2
            pos = (int(x), box[1])

        self.d.text(pos, text, font=self.font, fill=1)

if __name__ == '__main__':
    im = Image.new('1', (128,64))
    t = TextDraw(im)
    t.draw('hello', (0,0,127,10))
    t.draw('hello', (0,15,127,25), align='right')
    t.draw('hello', (0,30,127,40), align='center')
    im.save('/tmp/t.jpg')

