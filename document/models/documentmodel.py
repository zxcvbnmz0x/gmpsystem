# -*- coding: utf-8 -*-

from db.models import Documents


class DocumentModel(object):

    @staticmethod
    def get_document(autoid=0, *args, **kwargs):
        flat = True if len(args) == 1 else False
        if autoid:
            kwargs.update(autoid=autoid)
        if len(args):
            return Documents.objects.filter(**kwargs).values_list(*args, flat=flat)
        else:
            return Documents.objects.filter(**kwargs)

