# -*- coding: utf-8 -*-
from labrecord.models.checkitem import CheckItem as CI


class CheckItem(object):
    def __init__(self, parent=None):
        self.checkitem = CI()

    def get_checkitems(self, display_flag=False, *args, **kwargs):
        return self.checkitem.get_checkitems(display_flag, *args, **kwargs)

    def delete_check_item(self, autoid):
        return self.checkitem.delete_check_item(autoid)

    def update_check_item(self, autoid=None, **detail):
        return self.checkitem.update_check_item(autoid, **detail)
