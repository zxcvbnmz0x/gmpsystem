# -*- coding: utf-8 -*-
from lib.utils.saveexcept import SaveExcept
from django.db import transaction, connection
from db.models import Productdictionary, Productlabel, Producingplan, Linepost, \
    Linepostdocument, Forms, Eqrunnotes, Selfdefinedformat
from imageslib.controllers.image import Image
import user


class WorkshopModels(object):
    def __init__(self):
        super().__init__()

    def get_linepost(self, ppid):
        return Linepost.objects.filter(ppid=ppid).order_by('seqid')

    def get_linepostdocuments(self, lpid):
        return Linepostdocument.objects.filter(lpid__in=lpid).order_by('lpid', 'seqid')

    def get_form(self, aid):
        return Forms.objects.get(autoid=aid)

    def update_form(self, aid: int, content):
        return Forms.objects.filter(autoid=aid).update(format=content)

    def reset_form(self, aid: int):
        res = Forms.objects.get(autoid=aid)
        if res is not None:
            ori_content = Selfdefinedformat.object.get(autoid=res.selfid)

        return Forms.objects.filter(autoid=aid).update(format=ori_content)

