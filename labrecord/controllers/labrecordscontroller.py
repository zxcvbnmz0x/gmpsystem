# -*- coding: utf-8 -*-
from labrecord.models.labmodel import LabModel
from imageslib.imagesmodel import ImagesModel
from selfdefinedfirmat.controllers.selfdefinedformatcontroller import SelfdefinedformatController


class LabrecordsController(object):
    def __init__(self):
        self.SC = SelfdefinedformatController()

    def get_labrecord(self, flag=False, *args, **kwargs):
        return LabModel.get_labrecord(flag, *args, **kwargs)

    def get_labitem(self, flag=False, *args, **kwargs):
        return LabModel.get_labitem(flag, *args, **kwargs)

    def get_labimages(self, flag=False, kind=2, scid=0):
        values_list_rela = [
            'autoid', 'title', 'imageid', 'creatorid', 'creatorname',
            'createdate'
        ]
        key_dict_rela = {'kind': kind, 'scid': scid}
        res = ImagesModel.get_rela(flag, *values_list_rela, **key_dict_rela)
        if not len(res):
            return []
        img_list = []
        for item in res:
            img_list.append(item['imageid'])
        values_list_img = ['autoid', 'img', 'ext']
        key_dict_img = {'autoid__in': img_list}
        image_list = ImagesModel.get_img(flag, *values_list_img, **key_dict_img)
        for it in res:
            for value in image_list:
                if it['imageid'] == value['autoid']:
                    it.update({'image': value['img'], 'ext': value['ext']})
                    break
        return res

    def select_oricheckpaper(self, dictid, itemtype=0):
        if not dictid:
            return []
        values_list = ['sdfid']
        key_dict = {
            'dictid': dictid,
            'itemtype': itemtype
        }
        sdfid_list = LabModel.get_oricheckpapersetting(True, *values_list, **key_dict)
        if len(sdfid_list):
            values_list_sdf = ['autoid', 'kind', 'formatname']
            key_dict_sdf = {
                'autoid__in': sdfid_list
            }
            return self.SC.get_selfdefinedformat(False, *values_list_sdf, **key_dict_sdf)
        else:
            return []

    def get_selfdefineformat(self, flag=False, *args, **kwargs):
        return self.SC.get_selfdefinedformat(False, *args, **kwargs)

    def get_oricheckpaper(self, flag=False, *args, **kwargs):
        return LabModel.get_oricheckpaper(flag, *args, **kwargs)

    def get_paperno(self, lrid):
        return LabModel.get_paperno(lrid)

    def update_labrecord(self, autoid=0, *args, **kwargs):
        return LabModel.update_labrecord(autoid, *args, **kwargs)

    def delete_labrecord(self, autoid=0, *args, **kwargs):
        return LabModel.delete_labrecord(autoid, *args, **kwargs)

    def update_labitem(self, autoid=0, *args, **kwargs):
        return LabModel.update_labitem(autoid, *args, **kwargs)

    def delete_labitem(self, autoid=0, *args, **kwargs):
        return LabModel.delete_labitem(autoid, *args, **kwargs)

    def update_labimages(self, relakwargs, imgkwargs, relaid=0, imgid=0):
        return ImagesModel.update_img(relakwargs, imgkwargs, relaid, imgid)

    def update_oricheckpaper(self, autoid=0, sdfid_list:list=[], *args, **kwargs):
        if autoid:
            return LabModel.update_oricheckpaper(autoid, *args, **kwargs)
        detail_list = []
        if len(sdfid_list):
            for sdfid in sdfid_list:
                sdformat = self.SC.get_selfdefinedformat(False, autoid=sdfid)
                if len(sdformat) == 1:
                    kwargs['formname'] = sdformat[0].formatname
                    kwargs['formcontent'] = sdformat[0].format
                    detail_list.append(kwargs)
            return_list = []
            for item in detail_list:
                res = LabModel.update_oricheckpaper(**item)
                return_list.append(res)
            return return_list


    def delete_labimages(self, relaid, imgid):
        return ImagesModel.delete_img(relaid, imgid)

    def delete_oricheckpaper(self, id_list):
        return LabModel.delete_oricheckpaper(id_list)

    def get_data(self, table_num: int, display_flag=False, *args, **kwargs):
        table_str = TABLE_SET[table_num][0]
        err_msg = "查询" + TABLE_SET[table_num][1]
        return LabModel.get_data(
            table_str, err_msg, display_flag, *args, **kwargs
        )

    def update_data(self, table_num: int, condition={}, *args, **kwargs):
        table_str = TABLE_SET[table_num][0]
        err_msg = "更新" + TABLE_SET[table_num][1]
        return LabModel.update_data(
            table_str, err_msg, condition, *args, **kwargs
        )

    def delete_data(self, table_num: int, condition={}, *args, **kwargs):
        table_str = TABLE_SET[table_num][0]
        err_msg = "删除" + TABLE_SET[table_num][1]
        return LabModel.delete_data(
            table_str, err_msg, condition, *args, **kwargs
        )

TABLE_SET = [
    ('Labrecords', "检验报告"),
    ('Labrecordsdetail', "检验报告项目"),
    ('Originalcheckpaper', "原始检验记录"),
    ('Originalcheckpapersetting', "原始检验记录设置"),
    ('Checkitems', "检验项目"),
]