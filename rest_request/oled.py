#!/usr/bin/python
# -*- coding: <encoding name> -*-

import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

class Oled(object):
    oled = None
    def __init__(self, rst=24, dc=25, spi=None):
        if spi is None:
            spi = SPI.SpiDev(0, 0, max_speed_hz=8000000)
        self.oled = Adafruit_SSD1306.SSD1306_128_64(rst=rst, dc=dc, spi=spi)
        self.oled.begin()
        self.oled.clear()
        self.oled.display()

    def refresh(self, image):
        self.oled.image(image)
        self.oled.display()

    def size(self):
        return (self.oled.width, self.oled.height)

if __name__ == '__main__':
    oled = Oled()
    
    from PIL import Image
    image = Image.open('Logo2.bmp').convert('1')
    oled.refresh(image)
