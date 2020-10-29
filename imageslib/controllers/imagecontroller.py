# -*- coding: utf-8 -*-

from imageslib.models.imagemodel import Imagemodel
import user

class ImageController(object):

    def get_image(self, display_flag=False, *args, **kwargs):
        return Imagemodel.get_image(display_flag, *args, **kwargs)

    def delete_image(self, key_dict=None, *args, **kwargs):
        return Imagemodel.delete_image(key_dict, *args, **kwargs)

    def update_image(self, key_dict=None, *args, **kwargs):
        return Imagemodel.save_image(key_dict, *args, **kwargs)
