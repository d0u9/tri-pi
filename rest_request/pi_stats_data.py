#!/usr/bin/python
# -*- coding: utf-8 -*-

import psutil
import math

class PiStatsData(object):
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
        cpu = { 'percent': psutil.cpu_percent(),
                'count': psutil.cpu_count(),
                'freq': psutil.cpu_freq()[0],
              }

        mem = { 'memory': psutil.virtual_memory(),
                'swap': psutil.swap_memory(),
              }

        disk = []
        for p in psutil.disk_partitions():
            part = {}
            usage = psutil.disk_usage(p[1])
            part['device'] = p[0]
            part['mountpoint'] = p[1]
            part['fstype'] = p[2]
            part['total'] = usage[0]
            part['used'] = usage[1]
            part['free'] = usage[2]

            disk.append(part)

        network = {}
        for key, val in psutil.net_io_counters(pernic=True).items():
            stat = {}
            stat['bytes_sent'] = val[0]
            stat['bytes_recv'] = val[1]
            stat['packets_sent'] = val[2]
            stat['packets_recv'] = val[3]
            stat['errin'] = val[4]
            stat['errout'] = val[5]
            stat['dropin'] = val[6]
            stat['dropout'] = val[7]

            if stat['bytes_sent'] == 0 and stat['bytes_recv'] ==0:
                continue

            network[key] = {}
            network[key]['stat'] = stat

        for key, val in psutil.net_if_addrs().items():
            if key not in network:
                continue

            dev = {'addr': '', 'ipv4': []}
            for addr in val:
                if addr[0] == addr[0].AF_INET:
                    # tuple of (ipaddress, netmask, broadcast)
                    dev['ipv4'].append((addr[1], addr[2], addr[3]))

                if addr[0] == 17:
                    dev['addr'] = addr[1]

            if dev['ipv4'] == []:
                del(network[key])
            else:
                network[key]['addr'] = dev['addr']
                network[key]['ipv4'] = dev['ipv4']

        return { 'cpu': cpu, 'mem': mem, 'disk': disk, 'network': network }

    @staticmethod
    def humanfy(size_bytes):
       if size_bytes == 0:
           return "0B"
       size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
       i = int(math.floor(math.log(size_bytes, 1024)))
       p = math.pow(1024, i)
       s = round(size_bytes / p, 2)
       return "%.1f%s" % (s, size_name[i])

