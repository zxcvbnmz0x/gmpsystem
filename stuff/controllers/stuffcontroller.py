# -*- coding: utf-8 -*-
from stuff.models.stuffmodel import StuffModel


class StuffController():

    def get_stuff(self, display_flag=False, *args, **kwargs):
        return StuffModel.get_stuff(display_flag, *args, **kwargs)

    def get_stuffdict(self, display_flag=False, *args, **kwargs):
        return StuffModel.get_stuffdict(display_flag, *args, **kwargs)

    def get_prodstuff(self, display_flag=False, *args, **kwargs):
        return StuffModel.get_prodstuff(display_flag, *args, **kwargs)

    def get_Mprodstuff(self, ppid):
        return StuffModel.get_Mprodstuff(ppid)

    def get_stuffdrawpaper(self, display_flag=False, *args, **kwargs):
        return StuffModel.get_stuffdrawpaper(display_flag, *args, **kwargs)

    def update_stuffdrawpaper(self, autoid=0, *args, **kwargs):
        return StuffModel.update_stuffdrawpaper(autoid, *args, **kwargs)

    def update_productstuff(self, key_dict, *args, **kwargs):
        return StuffModel.update_productstuff(key_dict, *args, **kwargs)

