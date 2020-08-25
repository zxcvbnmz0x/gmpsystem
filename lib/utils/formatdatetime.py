# -*- coding: utf-8 -*-
import user
import datetime


def format_datetime(dtime: datetime):
    if dtime in (user.unsigndate, user.unsigntime, user.unsigndatetime) or str(
            dtime) in ('0000-00-00', '0000-00-00 00:00:00'):
        return ''
    else:
        return str(dtime)
