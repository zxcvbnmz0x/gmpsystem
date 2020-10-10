# -*- coding: utf-8 -*-

from qrcode.models.qrcodemodel import QrcodeModel


class QrcodeController():

    def get_qrcoderep(self, display_flag=False, *args, **kwargs):
        return QrcodeModel.get_qrcoderep(display_flag, *args, **kwargs)

    def update_qrcoderep(self,key_dict=None, *args, **kwargs):
        return QrcodeModel.update_qrcoderep(key_dict, *args, **kwargs)