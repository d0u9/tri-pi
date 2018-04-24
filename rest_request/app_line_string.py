#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageMath

from app_string import StringApp, StringDraw

class LineStringApp(StringApp):
    def __init__(self, display, config={}):
        super(LineStringApp, self).__init__(display, config=config)

        self.box = (0, 0, self.image.width-1, self.image.height-1)
        self.line_height = 10

        # each element in self.image_list is formatted ((x1, y1, x2, y2), imageObj)
        self.image_list = []
        self.draw_ = ImageDraw.Draw(self.image)
        self.max_height = 0
        self.current_screen = 0
        self.scroll_height = 10

    def set(self, font=None, font_size=None, box=None, line_height=None):
        self.font_name = self.font_name if font is None else font
        self.font_size = self.font_size if font_size is None else font_size
        self.box = self.box if box is None else box
        self.line_height = self.line_height if line_height is None else line_height

    def redraw(self, string, clear=False, blank_between_paragraph=True):
        self.str = string
        contents = self.wrap()
        i = 0

        width = self.box[2] - self.box[0]
        height = self.box[3] - self.box[1]
        self.max_height = max(self.max_height, self.box[3])

        image = Image.new('1', (width, height))
        draw = StringDraw(image, self.font)

        if clear:
            self.image_list = []

        for paragraph in contents:
            for line in paragraph:
                pos=(0, i * self.line_height)
                draw.redraw(line, self.font_name, self.font_size, pos)
                i += 1

            if blank_between_paragraph:
                pos=(0, i * self.line_height)
                draw.redraw('\n', self.font_name, self.font_size, pos)
                i += 1

        self.image_list.append((self.box, image))

    def refresh(self):
        max_width = 128
        max_height = self.max_height

        self.full_image = Image.new('1', (max_width, max_height))

        for fragment in self.image_list:
            self.full_image.paste(fragment[1], fragment[0])

        self.crop_creen()

    def crop_creen(self):
        crop_box = (0, self.current_screen, self.image.width, self.current_screen + self.image.height)
        self.image = self.full_image.crop(crop_box)

    def strlen_in_pixel(self, substr):
        f = ImageFont.truetype(self.font_name, self.font_size)
        return self.draw_.textsize(substr, font=f)[0]

    def test_pos(self, pos, substr):
        if self.strlen_in_pixel(substr[0:pos+1]) > (self.box[2] - self.box[0]):
            return True
        return False

    def wrap_len(self, substr):
        width = self.box[2] - self.box[0]
        if self.strlen_in_pixel(self.str) < width:
            return len(self.str)

        left, right = (0, len(self.str))
        while right - left > 1:
            mid = int((left + right) / 2)

            if self.strlen_in_pixel(substr[0: mid]) <= width:
                if self.test_pos(mid, substr) is True:
                    break
                else:
                    left = mid
            else:
                right = mid

        return mid

    def wrap(self):
        out = []
        width = self.box[2] - self.box[0]
        for substr in self.str.splitlines():
            start, pos = (0, 0)
            sub = []
            while start < len(substr):
                pos = self.wrap_len(substr[start:])
                sub.append(substr[start: start+pos])
                start += pos
            out.append(sub)

        return out

    def event_next(self):
        if self.current_screen + self.image.height > self.full_image.height:
            return

        self.current_screen += self.scroll_height
        self.crop_creen()
        self.show()

    def event_prev(self):
        if self.current_screen <= 0:
            self.current_screen = 0
            return

        self.current_screen -= self.scroll_height
        self.crop_creen()
        self.show()

