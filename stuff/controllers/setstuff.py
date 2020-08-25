# -*- coding: utf-8 -*-

from stuff.models.stuffmodel import StuffModel


class setStuff(object):
    def __init__(self, parent=None):
        self.SM = StuffModel()

    def update_stuff(self, autoid=None, **kwargs):
        return self.SM.update_stuff(autoid, **kwargs)
