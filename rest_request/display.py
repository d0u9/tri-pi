#!/usr/bin/python
# -*- coding: utf-8 -*-

import shutil
import os
import logging

class Display(object):
    def __init__(self):
        self.size = (0, 0)
        self.logger = logging.getLogger('rest_request')
        self.current_image = None

    def refresh(self, image):
        pass

    def trun_off(self):
        pass

    def trun_on(self):
        pass

try:
    import RPi.GPIO as GPIO
    import Adafruit_GPIO.SPI as SPI
    import Adafruit_SSD1306

    class DisplayOled(Display):
        def __init__(self):
            super(DisplayOled, self).__init__()

            self.rst_pin = 24
            self.dc_pin = 25
            self.spi_port = 0
            self.spi_dev_index = 0
            self.logger.info('DisplayOled: spi->rst = %d, spi->dc = %d, spi->port = %d, spi->dev = %d',
                             self.rst_pin, self.dc_pin, self.spi_port, self.spi_dev_index)
            self.spi = SPI.SpiDev(self.spi_port, self.spi_dev_index, max_speed_hz=8000000)
            self.oled = Adafruit_SSD1306.SSD1306_128_64(rst=self.rst_pin, dc=self.dc_pin, spi=self.spi)
            self.size = (self.oled.width, self.oled.height)
            self.oled.begin()
            self.oled.clear()
            self.oled.display()

        def refresh(self, image):
            self.current_image = image
            self.logger.debug('DisplayOled: refresh')
            self.oled.image(image)
            self.oled.display()

        def turn_off(self):
            self.oled.clear()
            self.oled.display()

        def turn_on(self):
            self.oled.image(self.current_image)
            self.oled.display()
except:
    pass


class DisplayFile(Display):
    def __init__(self, path):
        super(DisplayFile, self).__init__()

        self.logger.info('DisplayFile: path = %s', path)

        self.size = (128, 64)
        self.path = path
        self.file_index = 0

        try:
            shutil.rmtree(self.path)
        except:
            pass

        os.mkdir(self.path)

    def refresh(self, image):
        self.current_image = image
        self.logger.debug('DisplayFile: refresh, index = %d', self.file_index)
        image.save(os.path.join(self.path, str(self.file_index) + '.jpg'), 'JPEG')
        self.file_index += 1
