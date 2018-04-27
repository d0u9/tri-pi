#!/usr/bin/python
# -*- coding: utf-8 -*-

import psutil
import requests
import math
import os

from requests import ConnectionError

class ServerStatsData(object):
    @staticmethod
    def GetCpu():
        cpu_times = psutil.cpu_times()
        cpu_percent = psutil.cpu_percent()
        cpu_count = psutil.cpu_count()
        return {'times': cpu_times, 'percent': cpu_percent, 'count': cpu_count}

    @staticmethod
    def GetMem():
        pass

    @staticmethod
    def GetNetWork():
        pass

    @staticmethod
    def GetDisk():
        pass

    @staticmethod
    def GetAll():
        pass

    @staticmethod
    def GetExcerpt(config):
        server = config['server']
        url = os.path.join(server, 'excerpt')

        r = requests.get(url)

        return r.json()


    @staticmethod
    def humanfy(size_bytes):
       if size_bytes == 0:
           return "0B"
       size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
       i = int(math.floor(math.log(size_bytes, 1024)))
       p = math.pow(1024, i)
       s = round(size_bytes / p, 2)
       return "%.1f%s" % (s, size_name[i])

