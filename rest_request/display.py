#!/usr/bin/python
# -*- coding: <encoding name> -*-

from menu import Menu, Item

class Display(object):
    def __init__(self, menu, max_line):
        self.__stack__ = []
        self.menu = menu
        self.max_line = max_line
        self.current_index = 0
        self.top_line = 0

    def next(self):
        if self.current_index == self.menu.size() - 1:
            return

        self.current_index += 1
        if self.current_index >= self.top_line + self.max_line:
            self.top_line += 1

    def prev(self):
        if self.current_index == 0:
            return

        self.current_index -= 1
        if self.current_index < self.top_line:
            self.top_line -= 1

    def triger(self):
        self.__stack__.append((self.menu, self.current_index, self.top_line))
        item = self.menu.get_by_index(self.current_index)
        if isinstance(item, Menu):
            self.menu = item
            self.current_index = 0
            self.top_line = 0
        elif isinstance(item, Item):
            item.run()
            self.menu, self.current_index, self.top_line = self.__stack__.pop()
        else:
            raise TypeError

    def back(self):
        self.menu, self.current_index, self.top_line = self.__stack__.pop()

    def show(self):
        print('screen = {}'.format(self.menu.captions(self.top_line, self.max_line)))
        print('current = {}'.format(self.menu.get_by_index(self.current_index)))


if __name__ == '__main__':
    def cbs(args):
        print('Hello {}'.format(args))

    menu2 = Menu('menu2')
    menu2.add(('sub2-0', cbs, 'sub2-0'))
    menu2.add(('sub2-1', cbs, 'sub2-1'))
    menu2.add(('sub2-2', cbs, 'sub2-2'))

    menu1 = Menu('menu1')
    menu1.add(('sub1-0', cbs, 'sub1-0'))
    menu1.add(menu2)
    menu1.add(('sub1-1', cbs, 'sub1-1'))
    menu1.add(('sub1-2', cbs, 'sub1-2'))
    menu1.add(('sub1-3', cbs, 'sub1-3'))
    menu1.add(('sub1-4', cbs, 'sub1-4'))
    menu1.add(('sub1-5', cbs, 'sub1-5'))

    menu = Menu('root')
    menu.add(('test0', cbs, 'test0'))
    menu.add(menu1)
    menu.add(('test1', cbs, 'test1'))
    menu.add(('test2', cbs, 'test2'))
    menu.add(('test3', cbs, 'test3'))
    menu.add(('test4', cbs, 'test4'))
    menu.add(('test5', cbs, 'test5'))
    menu.add(('test6', cbs, 'test6'))
    menu.add(('test7', cbs, 'test7'))

    print('==== dump menu ====')
    menu.dump()
    print('==== dump menu ====', end='\n\n')

    d = Display(menu, 3)
    d.show()

    d.next()
    d.triger()
    d.next()
    d.triger()
    d.triger()
    d.back()
    d.back()
    d.next()
    d.triger()


