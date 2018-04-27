#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageMath

class ProgressBarDraw(object):
    def __init__(self, image):
        self.image = image

        self.d = ImageDraw.Draw(self.image)
        self.current = 0
        self.total = 0
        self.caption_fmt = ''
        self.box = (0, 0, 0, 0)

        self.font_name = 'font.ttf'
        self.font_size = 8
        self.caption_padding = 1
        self.caption_percent = False

    def set(self, box, current=0, total=100, caption_fmt='', caption_percent=False, font='font.ttf', font_size=8, caption_padding=1):
        if total < 0 or current < 0:
            self.total = self.current = 0

        if current > total:
            self.current = self.total = total

        self.total = total
        self.current = current

        if isinstance(box, tuple):
            self.box = box

        self.font_name = font
        self.font_size = font_size
        self.caption_fmt = caption_fmt
        self.caption_padding = caption_padding

        self.caption_percent = caption_percent

    def draw(self, auto_height=True, humanfy=lambda x: x):
        self.d.rectangle(self.box, outline=1)

        if self.caption_percent:
            caption = self.caption_fmt % (humanfy(self.current / self.total * 100))
        else:
            caption = self.caption_fmt % (humanfy(self.current), humanfy(self.total))

        fnt = ImageFont.truetype(self.font_name, self.font_size)
        size = self.d.textsize(caption, font=fnt)

        caption_pos = (self.box[2] - size[0], self.box[3] + self.caption_padding)
        self.d.text(caption_pos, caption, font=fnt, fill=1)

        if self.current != 0:
            width = (self.box[2] - self.box[0]) * (self.current / self.total) + self.box[0]
            fill_box = (self.box[0], self.box[1], width, self.box[3])
            self.d.rectangle(fill_box, fill=1)

        return (self.box[0], self.box[1], self.box[2], self.box[3] + self.caption_padding + size[1])


if __name__ == '__main__':
    im = Image.new('1', (128,64))
    pb = ProgressBarDraw(im)
    pb.set((5,5,120,15), total=100, current=10, caption_fmt='%d/%d MB')
    pb.draw()
    pb.set((5,30,120,40), total=100, current=10, caption_percent=True, caption_fmt='%d%%')
    pb.draw()

    im.save('/tmp/pb.jpg')

