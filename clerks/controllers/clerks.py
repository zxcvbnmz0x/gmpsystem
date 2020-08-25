# -*- coding: utf-8 -*-

from clerks.models.deptclerkmodel import DeptClerkModel


class Clerks(object):
    def __init__(self):
        self.DC = DeptClerkModel()

    def get_clerks(self, clerkid, *args, **kwargs):
        return self.DC.get_clerks(clerkid, *args, **kwargs)
