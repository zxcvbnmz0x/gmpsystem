# -*- coding: utf-8 -*-

from linepost.models.linepostmodel import LinepostModel
from productline.controllers.productlineconroller import ProductLineConroller
from document.controllers.documentcontroller import DocumentController
from cleanfirmity.controllers.cleanfirmitycontroller import CleanfirmityController
from django.db import transaction

class LinepostController(object):

    def __int__(self):
        super(LinepostController, self).__init__()

    # 获得岗位信息
    def get_linepost(self, autoid, *args, **kwargs):
        return LinepostModel.get_linepost(autoid, *args, **kwargs)

    def get_spareroomlist(self, plid, seqid, postname):
        res = LinepostModel.get_spareroomlist(plid, seqid, postname)
        return list(res)[0]

    # 获得岗位工人
    def get_worker(self, plid, seqid, postname, *args, **kwargs):
        return LinepostModel.get_worker(plid, seqid, postname, *args, **kwargs)

    # 获得岗位文档
    def get_gmpfile(self, plid, seqid, postname, *args, **kwargs):
        pline = ProductLineConroller()
        # wfid,岗位在workflow表中的autoid
        wfid = pline.get_workflow(plid, 'autoid', seqid=seqid, postname=postname)
        # 当前岗位文档的autoid，对应document表中的autoid
        fileid = LinepostModel.get_gmpfile(list(wfid), 'docid')
        doc = DocumentController()
        return doc.get_document(0, *args, autoid__in=list(fileid))

    # 开始岗位，岗位开始后需要刷新该岗位的副本
    def start_linepost(self, lpid, rname, *args, **kwargs):
        CC = CleanfirmityController()
        with transaction.atomic():
            last_post_id = LinepostModel.start_linepost(lpid, rname, *args, **kwargs)
            if last_post_id > 0:
                ori_cl = CC.get_confirmity(lpid=last_post_id, iscopy=0)
                if len(ori_cl):
                    # 若这个岗位存在多次清场，则使用最后一个正本
                    ori_detail = list(ori_cl)[-1]
                    copy_data = {
                        'origid': ori_detail.autoid,
                        'roomname': rname,
                        'lastprodid': ori_detail.prodid,
                        'lastprodname': ori_detail.prodname,
                        'lastbatchno': ori_detail.batchno,
                        'cleanerid': ori_detail.cleanerid,
                        'cleanername': ori_detail.cleanername,
                        'cleandate': ori_detail.cleandate,
                        'checkerid': ori_detail.checkerid,
                        'checkername': ori_detail.checkername,
                        'checkdate': ori_detail.checkdate,
                        'validdate': ori_detail.validdate,
                    }
                    condition = {
                        'lpid': lpid,
                        'iscopy': 1
                    }
                    res = CC.update_confirmity(condition, **copy_data)
            return True

    # 结束岗位
    def end_linepost(self, lpid=0, *args, **kwargs):
        return LinepostModel.end_linepost(lpid, *args, **kwargs)
