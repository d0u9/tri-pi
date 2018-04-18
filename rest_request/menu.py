#!/usr/bin/python
# -*- coding: <encoding name> -*-

class Item(object):
    def __init__(self, caption, callback, args=None):
        self.caption = caption
        self.cb = callback
        self.args = args

    def run(self):
        self.cb(self.args)

    def __str__(self):
        return '{}: cb={}, args={}'.format(self.caption, self.cb, self.args)

    def dump(self):
        print(self)

class Menu(object):
    def __init__(self, caption):
        self.list = []
        self.caption = caption

    def add(self, param):
        if isinstance(param, tuple):
            item = Item(param[0], param[1], param[2])
            self.list.append(item)
        elif isinstance(param, Item):
            self.list.append(param)
        elif isinstance(param, Menu):
            self.list.append(param)
        else:
            raise TypeError

    def get_by_index(self, index):
        return self.list[index]

    def captions(self, start, offset=1):
        return [i.caption for i in self.list[start: start+offset]]

    def size(self):
        return len(self.list)

    def __str__(self):
        return '---- submenu: ----'

    def dump(self, indent=0):
        for item in self.list:
            for i in range(indent):
                print('\t', end='')

            if isinstance(item, Item):
                item.dump()
            elif isinstance(item, Menu):
                print('\t------ submenu: %s ------' %(item.caption))
                item.dump(indent + 1)

if __name__ == '__main__':
    def cbs(args):
        print('Hello: ', args)

    item = Item('sub1-1', cbs, 'sub1-1')

    menu2 = Menu('submenu')
    menu2.add(('sub1-0', cbs, 'sub1-0'))
    menu2.add(item)

    menu = Menu('root')
    menu.add(('test0', cbs, None))
    menu.add(menu2)

    menu.dump()

    c = menu2.captions(0, 3)
    print(c)
