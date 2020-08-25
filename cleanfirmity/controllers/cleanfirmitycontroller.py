# -*- coding: utf-8 -*-

from cleanfirmity.models.cleanfirmitymodels import CleanfirmityModels


class CleanfirmityController(object):

    def get_confirmity(self, autoid=0, *args, **kwargs):
        return CleanfirmityModels.get_cleanfirmity(autoid, *args, **kwargs)

    def update_confirmity(self, condition: dict, *args, **kwargs):
        return CleanfirmityModels.update_cleanfirmity(condition, *args, **kwargs)
