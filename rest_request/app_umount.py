#!/usr/bin/python
# -*- coding: utf-8 -*-

from app import BackSchedule
from app_menu import MenuApp
from app_string import StringApp

class UmountApp(MenuApp):
    def __init__(self, display):
        self.menu_app = [('Movies', self.umount_movies),
                         ('Videos', self.umount_videos),
                         ('Games', self.umount_games),
                         ('Backup All', self.umount_backup_all)]
        menu = [ i[0] for i in self.menu_app ]
        super(UmountApp, self).__init__(display, menu)

        self.logger.debug('UmountApp::__init__, menu = %s', self.menu_app)

    def event_trigger(self):
        func = self.menu_app[self.current][1]
        self.logger.debug('UmountApp::event_trigger, cb_func = %s', func)

        ret = func()

        app = StringApp(self.display)
        app.redraw(ret)

        return app

    def event_back(self):
        self.logger.debug('UmountApp::event_back, retrun from this app')
        return BackSchedule()

    def umount_movies(self):
        self.logger.info('UmountApp::umount_movies, umounting movies disk')
        string = 'success'
        return string

    def umount_videos(self):
        self.logger.info('UmountApp::umount_videos, umounting videos disk')
        print('umount videos')

        return 'videos'

    def umount_games(self):
        self.logger.info('UmountApp::umount_games, umounting games disk')

        return 'games'

    def umount_backup_all(self):
        self.logger.info('UmountApp::umount_backup_all, umounting backup_all disk')

        return 'backup_all'

