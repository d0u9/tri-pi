#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageMath

import string

image = Image.new('1', (128, 64))
draw = ImageDraw.Draw(image)

f = ImageFont.truetype('../font.ttf', 8)

text_in = string.printable
text_in = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXx\nYyZz0123456789,./<>?'

def strlen_in_pixel(text):
    return draw.textsize(text, font=f)[0]

def test_pos(text, pos, max_width):
    if strlen_in_pixel(text[0: pos + 1]) > max_width:
        return True
    return False

def wrap_len(text, width):
    if strlen_in_pixel(text) < width:
        return len(text)

    left, right = (0, len(text))
    while right - left > 1:
        mid = int((left + right) / 2)

        if strlen_in_pixel(text[0: mid]) <= width:
            if test_pos(text, mid, width) is True:
                break
            else:
                left = mid
        else:
            right = mid

    return mid

def wrap(text, width):
    out = []
    for substr in text.splitlines():
        start, pos = (0, 0)
        sub = []
        while start < len(substr):
            pos = wrap_len(substr[start:], width)
            sub.append(substr[start: start+pos])
            start += pos
        out.append(sub)

    return out

print('-----')
o = wrap(text_in, 64)
print(o)

for paragraph in o:
    for line in paragraph:
        if strlen_in_pixel(line) > 64:
            print(strlen_in_pixel(line))
            print('error')
