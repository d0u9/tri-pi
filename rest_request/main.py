#!/usr/bin/python
# -*- coding: <encoding name> -*-

import RPi.GPIO as GPIO
import time
import requests
import logging
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from logging.handlers import RotatingFileHandler
from threading import Timer
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageMath

LED_R = 16
LED_G = 20
LED_B = 21

BTN_1 = 6   # Movies
BTN_2 = 13  # Videso
BTN_3 = 19  # Games
BTN_4 = 26  # Backup

# Raspberry Pi pin configuration:
# We use hardware SPI
RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

TIME_TO_TURN_LEDS_OFF = 5
TIMER = None
LOGO_SHOW_TIME = 1
FONT_SIZE = 8

REST_SERVER = 'http://tri-server:8080/'

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

def leds_off():
    GPIO.output([LED_R, LED_G, LED_B], GPIO.LOW)


def handle(pin):
    time.sleep(0.01)
    if GPIO.input(pin) is not 0:
        return

    global TIMER
    if TIMER is not None:
        TIMER.cancel()

    GPIO.output([LED_R, LED_G], GPIO.LOW)
    GPIO.output(LED_B, GPIO.HIGH)

    label = ''
    if pin is BTN_1:
        label = 'movies'
    elif pin is BTN_2:
        label = 'videos'
    elif pin is BTN_3:
        label = 'games'
    elif pin is BTN_4:
        label = 'backup_all'
    else:
        logger.error('Unknown button is pressed, pin = %d', pin)
        GPIO.output(LED_R, GPIO.HIGH)
        return

    logger.info('Umount disk: %s', label)

    url = REST_SERVER + 'umount/' + label
    logger.info('request url: %s', url)

    r = requests.get(url)
    logger.info('Server status code: %d', r.status_code)
    logger.info('Server msg: %s', r.text)

    GPIO.output(LED_B, GPIO.LOW)
    if r.status_code == 200:
        GPIO.output(LED_G, GPIO.HIGH)
    elif r.status_code == 404:
        GPIO.output(LED_G, GPIO.HIGH)
        GPIO.output(LED_R, GPIO.HIGH)
    else:
        GPIO.output(LED_R, GPIO.HIGH)

    TIMER = Timer(TIME_TO_TURN_LEDS_OFF, leds_off)
    TIMER.start()


if __name__ == '__main__':
    logger.info('Starting...')

    disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))
    disp.begin()

    # Get display width and height.
    width = disp.width
    height = disp.height

    disp.clear()
    disp.display()

    image = Image.open('Logo2.bmp').convert('1')
    disp.image(image)
    disp.display()

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup([BTN_1, BTN_2, BTN_3, BTN_4], GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    GPIO.setup([LED_R, LED_G, LED_B], GPIO.OUT, initial=GPIO.LOW)

    GPIO.add_event_detect(BTN_1, GPIO.FALLING, handle)
    GPIO.add_event_detect(BTN_2, GPIO.FALLING, handle)
    GPIO.add_event_detect(BTN_3, GPIO.FALLING, handle)
    GPIO.add_event_detect(BTN_4, GPIO.FALLING, handle)

    time.sleep(LOGO_SHOW_TIME)
    disp.clear()

    font = ImageFont.truetype('font.ttf', FONT_SIZE)

    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)

    menu = ['Get up early',
            'Goto school',
            'Rest',
            'Study',
            'Excise',
            'Sleep']

    for i in range(0, 6):
        #draw.text((2, 2 + (FONT_SIZE + 2) * i), 'ABCDEF ?*&^ abcedf', font=font, fill=1)
        draw.text((2, 2 + (FONT_SIZE + 2) * i), menu[i], font=font, fill=1)

    disp.image(image)
    disp.display()

    time.sleep(1)

    while True:
        for i in range(0, 6):
            box = (0, 3 + (10 * i), width-1, 12 + (10 * i))
            bef = image.crop(box)
            aft = ImageMath.eval('255-(a)', a=bef)
            image.paste(aft, box=box)
            disp.image(image)
            disp.display()
            time.sleep(1)
            image.paste(bef, box=box)
            disp.image(image)
            disp.display()

        time.sleep(1)

