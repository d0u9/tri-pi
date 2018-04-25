#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import os
import json

from app import BackSchedule
from app_menu import MenuApp
from app_line_string import LineStringApp

class UmountApp(MenuApp):
    def __init__(self, display, config):
        self.menu_app = [('Movies',     self.umount_movies),
                         ('Videos',     self.umount_videos),
                         ('Games',      self.umount_games),
                         ('Backup All', self.umount_backup_all)]
        menu = [ i[0] for i in self.menu_app ]
        super(UmountApp, self).__init__(display, config=config, menu=menu)

        self.logger.debug('UmountApp::__init__, menu = %s', self.menu_app)
        self.config = config.get('app_umount', None)
        self.server = self.config['server']

    def event_trigger(self):
        func = self.menu_app[self.current][1]
        self.logger.debug('UmountApp::event_trigger, cb_func = %s', func)

        retcode, retmsg = func()
        #  retcode, retmsg = (True, 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz')

        app = LineStringApp(self.display)
        app.set(font_size=16, box=(5, 1, 128, 20), line_height=18)
        if retcode:
            app.redraw('OK')
        else:
            app.redraw('Error Msg')

        app.set(font_size=8, box=(5, 21, 128-5, 300), line_height=10)
        app.redraw(retmsg)
        app.refresh()

        return app

    def event_back(self):
        self.logger.debug('UmountApp::event_back, retrun from this app')
        return BackSchedule()

    def rest_request(self, label):
        self.logger.debug('UmountApp::rest_request, umounting movies disk')
        url = os.path.join(self.server, label)
        self.logger.debug('UmountApp::rest_request, request url = %s', url)
        try:
            r = requests.get(url)
        except requests.ConnectionError as e:
            return (False, str(e))

        if r.status_code == 200:
            self.logger.info('UmountApp::rest_request, umount movie successfully(200)')
            return (True, 'Umount {} OK'.format(label))
        elif r.status_code == 404:
            self.logger.error('UmountApp::rest_request, umount movies error(404), %s', r.text)
            return (False, json.loads(r.text)['error'])
        else:
            self.logger.error('UmountApp::rest_request, umount movies error(NaN), %s', r.text)
            return (False, json.loads(r.text)['error'])

    def umount_movies(self):
        self.logger.debug('UmountApp::umount_movies, umounting videos disk')
        return self.rest_request('movies')

    def umount_videos(self):
        self.logger.debug('UmountApp::umount_videos, umounting videos disk')
        return self.rest_request('videos')

    def umount_games(self):
        self.logger.debug('UmountApp::umount_games, umounting games disk')
        return self.rest_request('games')

    def umount_backup_all(self):
        self.logger.debug('UmountApp::umount_backup_all, umounting backup_all disk')
        return self.rest_request('backup_all')

