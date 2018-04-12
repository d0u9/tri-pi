#!/usr/bin/python
# -*- coding: <encoding name> -*-

import RPi.GPIO as GPIO
import time
import requests
import logging

from logging.handlers import RotatingFileHandler
from threading import Timer

LED_R = 11
LED_G = 13
LED_B = 15

BTN_1 = 12  # Movies
BTN_2 = 16  # Videso
BTN_3 = 18  # Games
BTN_4 = 22  # Backup

TIME_TO_TURN_LEDS_OFF = 5
TIMER = None

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
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup([BTN_1, BTN_2, BTN_3, BTN_4], GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    GPIO.setup([LED_R, LED_G, LED_B], GPIO.OUT, initial=GPIO.LOW)

    GPIO.add_event_detect(BTN_1, GPIO.FALLING, handle)
    GPIO.add_event_detect(BTN_2, GPIO.FALLING, handle)
    GPIO.add_event_detect(BTN_3, GPIO.FALLING, handle)
    GPIO.add_event_detect(BTN_4, GPIO.FALLING, handle)

    while True:
        time.sleep(1e6)

