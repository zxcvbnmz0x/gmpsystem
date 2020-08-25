# -*- coding: utf-8 -*-
from stuff.models.stuffmodel import StuffModel


class StuffController(object):
    def __init__(self):
        pass

    def get_stuff(self, autoid):
        return StuffModel.get_stuff(autoid)

    def get_prodstuff(self, flag=0, *args, **kwargs):
        return StuffModel.get_prodstuff(flag, *args, **kwargs)

    def get_Mprodstuff(self, ppid):
        return StuffModel.get_Mprodstuff(ppid)

    def get_stuffdrawpaper(self, *args, **kwargs):
        return StuffModel.get_stuffdrawpaper(*args, **kwargs)

    def update_stuffdrawpaper(self, autoid=0, *args, **kwargs):
        return StuffModel.update_stuffdrawpaper(autoid, *args, **kwargs)
