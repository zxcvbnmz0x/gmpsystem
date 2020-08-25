# -*- coding: utf-8 -*-

from db.models import Imagelib


class Imagemodel(object):

    def get_image(sellf, autoid=0, **kwargs):
        if autoid:
            kwargs.update(autoid=autoid)
        return Imagelib.objects.filter(**kwargs)

    def delete_image(self, autoid=0, *args):
        return Imagelib.objects.filter(autoid__in=autoid).delete()

    def save_image(self, autoid=None, imagedetail=None, **kwargs):
        if autoid:
            return Imagelib.objects.filter(autoid=autoid).update(**imagedetail)
        else:
            return Imagelib.objects.create(**imagedetail)
