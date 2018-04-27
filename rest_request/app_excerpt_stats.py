#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from threading import Timer
from requests import ConnectionError

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from app import BackSchedule
from app_line_string import LineStringApp
from draw_progress_bar import ProgressBarDraw

class StatsExcerptApp(LineStringApp):
    def __init__(self, display, devs, config={}):
        super(StatsExcerptApp, self).__init__(display, devs, config)

        self.timer = None
        self.data_fetcher = None
        self.exerpt = None
        self.refresh_interval = 2

    def error_handler(self, msg):
        self.logger.error('StatsExcerptApp::error_handler, %s', str(msg))
        self.set(font_size=16, box=(5, 1, 128, 20), line_height=18)
        self.redraw('Error')
        self.set(font_size=8, box=(5, 21, 128-5, 300), line_height=10)
        self.redraw(str(msg))

        if self.timer is not None:
            self.timer.cancel()

        self.refresh()
        self.show()


    def draw_image(self):
        if self.data_fetcher is None:
            self.error_handler('No data fetcher specified')
            return

        try:
            data = self.data_fetcher.GetExcerpt(self.config['app_excerpt_stats'])
        except ConnectionError as e:
            self.error_handler(str(e))
            return

        if self.exerpt is None:
            self.exerpt = data

        line_height = 10
        line_height_caption = 18
        section_padding = 3
        top = 1
        left = 5
        right = 127 - left

        # CPU
        box = (left, top, right, top+line_height_caption)
        self.set(font='fix.ttf', font_size=16, box=box, line_height=line_height_caption)
        self.redraw('CPU')
        top += line_height_caption

        box = (left, top, right, top + 100)
        self.set(font='font.ttf', font_size=8, box=box, line_height=line_height)
        string = 'Core: {}\nFreq: {}' \
                 .format(data['cpu']['count'], data['cpu']['freq'])
        act_box = self.redraw(string, blank_between_paragraph=False)
        top += (act_box[3] - act_box[1]) + section_padding

        box = (left, top, right, top + 100)
        act_box = self.add_progress_bar(box=box,
                                        total=100, current=data['cpu']['percent'],
                                        fmt='Load: %.1f %%', percent=True)
        top += (act_box[3] - act_box[1])

        # Mem
        mem = data['mem']
        top += section_padding

        box = (left, top, right, top+line_height_caption)
        self.set(font='fix.ttf', font_size=16, box=box, line_height=line_height_caption)
        self.redraw('MEM')
        top += line_height_caption

        box = (left, top, right, top + 100)
        act_box = self.add_progress_bar(box=box,
                                        total=mem['memory'][0], current=mem['memory'][1],
                                        fmt='memory: %s / %s', humanfy=self.data_fetcher.humanfy)
        top += (act_box[3] - act_box[1])

        box = (left, top, right, top + 100)
        act_box = self.add_progress_bar(box=box,
                                        total=mem['swap'][0], current=mem['swap'][1],
                                        fmt='swap: %s / %s', humanfy=self.data_fetcher.humanfy)
        top += (act_box[3] - act_box[1])

        # Disk
        disk = data['disk']
        top += section_padding

        box = (left, top, right, top+line_height_caption)
        self.set(font='fix.ttf', font_size=16, box=box, line_height=line_height_caption)
        self.redraw('DISK')
        top += line_height_caption

        for d in disk:
            box = (left, top, right, top + 100)
            self.set(font='font.ttf', font_size=8, box=box, line_height=line_height)
            string = 'Dev: {}\nMP: {}\nType: {}' \
                     .format(d['device'], d['mountpoint'], d['fstype'])
            act_box = self.redraw(string, blank_between_paragraph=False)
            top += (act_box[3] - act_box[1]) + section_padding

            box = (left, top, right, top + 100)
            act_box = self.add_progress_bar(box=box,
                                            total=d['total'], current=d['used'],
                                            fmt='%s/%s',
                                            humanfy=self.data_fetcher.humanfy)
            top += (act_box[3] - act_box[1]) + section_padding * 2

        # Disk
        network = data['network']
        top += section_padding

        box = (left, top, right, top+line_height_caption)
        self.set(font='fix.ttf', font_size=16, box=box, line_height=line_height_caption)
        self.redraw('NETWORK')
        top += line_height_caption

        for key, val in network.items():
            dev = network[key]
            box = (left, top, right, top + 100)
            self.set(font='font.ttf', font_size=8, box=box, line_height=line_height)
            act_box = self.redraw('== {} =='.format(key))
            top += (act_box[3] - act_box[1]) + section_padding

            box = (left, top, right, top + 100)
            self.set(font='font.ttf', font_size=8, box=box, line_height=line_height)
            act_box = self.redraw('MAC: {}'.format(dev['addr']))
            top += (act_box[3] - act_box[1]) + section_padding

            for ip in dev['ipv4']:
                box = (left, top, right, top + 100)
                self.set(font='font.ttf', font_size=8, box=box, line_height=line_height)
                act_box = self.redraw('IP: {}'.format(ip[0]))
                top += (act_box[3] - act_box[1]) + section_padding

                box = (left, top, right, top + 100)
                self.set(font='font.ttf', font_size=8, box=box, line_height=line_height)
                act_box = self.redraw('MASK: {}'.format(ip[1]))
                top += (act_box[3] - act_box[1]) + section_padding

                box = (left, top, right, top + 100)
                self.set(font='font.ttf', font_size=8, box=box, line_height=line_height)
                act_box = self.redraw('BROAD: {}'.format(ip[2]))
                top += (act_box[3] - act_box[1]) + section_padding

            send_bytes_diff = dev['stat']['bytes_sent'] - self.exerpt['network'][key]['stat']['bytes_sent']
            recv_bytes_diff = dev['stat']['bytes_recv'] - self.exerpt['network'][key]['stat']['bytes_recv']

            send_speed = self.data_fetcher.humanfy(send_bytes_diff / self.refresh_interval / 8)
            recv_spped = self.data_fetcher.humanfy(recv_bytes_diff / self.refresh_interval / 8)

            box = (left, top, right, top + 100)
            self.set(font='font.ttf', font_size=8, box=box, line_height=line_height)
            act_box = self.redraw('up: {}/s'.format(send_speed))
            top += (act_box[3] - act_box[1]) + section_padding

            box = (left, top, right, top + 100)
            self.set(font='font.ttf', font_size=8, box=box, line_height=line_height)
            act_box = self.redraw('down: {}/s'.format(send_speed))
            top += (act_box[3] - act_box[1]) + section_padding

        self.refresh()
        self.show()

    def add_progress_bar(self, box, total, current, fmt, percent=False, humanfy=lambda x: x):
        subim_width = box[2] - box[0]
        subim_height = box[3] - box[1]
        im = Image.new('1', (subim_width, subim_height))
        pb_draw = ProgressBarDraw(im)
        pb_draw.set((0, 0, subim_width-1, 10), total=total, current=current, caption_percent=percent, caption_fmt=fmt)
        act_box = pb_draw.draw(humanfy=humanfy)
        self.append_image((box[0], box[1], box[2], box[1] + act_box[3]), im)

        return act_box

    def run(self):
        self.draw_image()
        self.timer = Timer(3, self.timer_cb)
        self.timer.start()

    def timer_cb(self):
        self.draw_image()
        self.timer = Timer(self.refresh_interval, self.timer_cb)
        self.timer.start()

    def set_data_fetcher(self, data_fetcher):
        self.data_fetcher = data_fetcher

    def event_back(self):
        if self.timer is not None:
            self.timer.cancel()

        return BackSchedule()
