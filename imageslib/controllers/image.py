# -*- coding: utf-8 -*-

from imageslib.models.imagemodel import Imagemodel
import user

class Image(object):
    def __init__(self):
        self.IM = Imagemodel()

    def get_image(self, autoid=0, **kwargs):
        return self.IM.get_image(autoid, **kwargs)

    def delete_image(self, autoid, *args):
        return self.IM.delete_image(autoid)

    def save_image(self, autoid=None, imagedetail=None, *args, **kwargs):
        return self.IM.save_image(autoid, imagedetail, *args, **kwargs)
