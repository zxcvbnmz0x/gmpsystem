# -*- coding: utf-8 -*-

from warehouse.models.warehousemodel import WarehouseModel
from stuff.controllers.stuffcontroller import StuffController
from workshop.controllers.workshopcontroller import WorkshopController
from supplyer.controllers.supplyercontroller import SupplyerController
from sale.controllers.salecontroller import SaleController
from product.controllers.productcontroller import ProductController
from django.db.models import Q

from django.db import transaction

import datetime

import operator
from functools import reduce

import user


class WarehouseController(object):

    def __init__(self):
        self.SC = StuffController()
        self.SLC = SaleController()
        self.SP = SupplyerController()
        self.WM = WarehouseModel()
        self.WC = WorkshopController()
        self.PC = ProductController()

    def get_stuffdrawpaper(self, *args, **kwargs):
        res = self.SC.get_stuffdrawpaper(*args, **kwargs)
        if len(res):
            ppid_list = list()
            for item in res:
                ppid_list.append(item.ppid)
            value_tuple = (
                'autoid', 'prodid', 'prodname', 'spec', 'package', 'batchno')
            prod_info_tuple = self.WM.get_producingplan(*value_tuple,
                                                        autoid__in=set(
                                                            ppid_list))
            for item in res:
                for it in prod_info_tuple:
                    if item.ppid == it[0]:
                        item.prod = it[1] + ' ' + it[2]
                        item.spec = it[3]
                        item.package = it[4]
                        item.batchno = it[5]
            return res
        else:
            return []

    def get_stuffrepository(self, display_flag=False, *args, **kwargs):
        return self.WM.get_stuffrepository(display_flag, *args, **kwargs)
        """res = self.WM.get_stuffrepository(flag, *args, **kwargs)
        supid_list = []
        if len(res):
            for item in res:
                supid_list.append(item['supid'])
            supplyers = self.SP.get_supply(('supid', 'supname'), supid__in=set(supid_list))
            for item in res:
                item['supname'] = ''
                for supplyer in supplyers:
                    if item['supid'] == supplyer[0]:
                        item['supname'] = supplyer[1]
                        break
        return res
        """

    def update_stuffrepository(self, autoid=None, *args, **kwargs):
        return WarehouseModel.update_stuffrepository(autoid, *args, **kwargs)

    def update_stuffrepository_amount(self, *args, **kwargs):
        return WarehouseModel.update_stuffrepository_amount(*args, **kwargs)

    def get_productputoutpaper(self, display_flag=False, *args, **kwargs):
        return WarehouseModel.get_productputoutpaper(display_flag, *args,
                                                     **kwargs)

    def update_productputoutpaper(self, autoid=None, *args, **kwargs):
        return WarehouseModel.update_productputoutpaper(autoid, *args, **kwargs)

    def delete_productputoutpaper(self, autoid=None, *args, **kwargs):
        return WarehouseModel.delete_productputoutpaper(autoid, *args, **kwargs)

    def get_prodwithdrawnote(self, display_flag=False, *args, **kwargs):
        return WarehouseModel.get_prodwithdrawnote(display_flag, *args,
                                                   **kwargs)

    def update_prodwithdrawnote(self, autoid, *args, **kwargs):
        return WarehouseModel.update_prodwithdrawnote(autoid, *args, **kwargs)

    def delete_prodwithdrawnote(self, autoid, *args, **kwargs):
        return WarehouseModel.delete_prodwithdrawnote(autoid, *args, **kwargs)

    def get_ppopqrcode(self, display_flag=False, *args, **kwargs):
        return WarehouseModel.get_ppopqrcode(display_flag, *args, **kwargs)

    def update_ppopqrcode(self, autoid, *args, **kwargs):
        return WarehouseModel.update_ppopqrcode(autoid, *args, **kwargs)

    def delete_ppopqrcode(self, autoid, *args, **kwargs):
        return WarehouseModel.delete_ppopqrcode(autoid, *args, **kwargs)

    def get_pwqrcode(self, display_flag=False, *args, **kwargs):
        return WarehouseModel.get_pwqrcode(display_flag, *args, **kwargs)

    def update_pwqrcode(self, autoid, *args, **kwargs):
        return WarehouseModel.update_pwqrcode(autoid, *args, **kwargs)

    def delete_pwqrcode(self, autoid, *args, **kwargs):
        return WarehouseModel.delete_pwqrcode(autoid, *args, **kwargs)

    def get_stuffcheckin(self, display_flag=False, *args, **kwargs):
        return WarehouseModel.get_stuffcheckin(display_flag, *args, **kwargs)

    def update_stuffcheckin(self, autoid, *args, **kwargs):
        return WarehouseModel.update_stuffcheckin(autoid, *args, **kwargs)

    def new_stuffcheckin(self, ppid, *args, **kwargs):
        detail = dict()
        key_dict = {'ppid': ppid}
        stuff_query = self.SP.get_purchstuff(
            False, *VALUES_TUPLE_PPLIST, **key_dict
        )
        if not len(stuff_query):
            return
        stuff_list = list(stuff_query)

        with transaction.atomic():
            p1 = transaction.savepoint()
            res = WarehouseModel.update_stuffcheckin(None, *args, **kwargs)

            for item in stuff_list:
                if item['amount'] - item['arrivedamount'] <= 0:
                    continue
                detail['paperno'] = res.paperno
                detail['papertype'] = 0
                detail['makedate'] = user.now_date
                detail['expireddate'] = user.now_date + datetime.timedelta(
                    days=item['expireddays']
                )
                detail['checkindate'] = user.now_date
                detail['amount'] = item['amount'] - item['arrivedamount']
                detail['piamount'] = item['amount'] - item['arrivedamount']
                detail['supid'] = kwargs['supid']
                detail['supname'] = kwargs['supname']
                del item['amount']
                del item['arrivedamount']
                del item['expireddays']
                detail.update(item)
                WarehouseModel.update_stuffcheckinlist(None, **detail)

    def delete_stuffcheckin(self, autoid, *args, **kwargs):
        return WarehouseModel.delete_stuffcheckin(autoid, *args, **kwargs)

    def get_stuffcheckinlist(self, display_flag=False, *args, **kwargs):
        return WarehouseModel.get_stuffcheckinlist(display_flag, *args,
                                                   **kwargs)

    def update_stuffcheckinlist(self, autoid, *args, **kwargs):
        return WarehouseModel.update_stuffcheckinlist(autoid, *args, **kwargs)

    def delete_stuffcheckinlist(self, autoid, *args, **kwargs):
        return WarehouseModel.delete_stuffcheckinlist(autoid, *args, **kwargs)

    def get_productrepository(self, display_flag=False, *args, **kwargs):
        return WarehouseModel.get_productrepository(display_flag, *args,
                                                    **kwargs)

    def update_productrepository(self, autoid, *args, **kwargs):
        return WarehouseModel.update_productrepository(autoid, *args, **kwargs)

    def delete_productrepository(self, autoid, *args, **kwargs):
        return WarehouseModel.delete_productrepository(autoid, *args, **kwargs)

    def find_prodqrcode(self, qrcode):
        """ 产品二维码中是否找到输入的二维码(qrcode)
        返回4个参数
        第一个参数
            0: 找到二维码且（全部）未使用
            1: 找到二维码但（全部）已被使用
            2: 找到二维码但（部分）已被使用
            3： 找不到二维码
        第二个参数
            二维码对应的数量
        第三个参数
            二维码所在的ppid,选择结果集中的第一个ppid
        第四个二维码
            二维码所在的batchno,选择结果集的第一个batchno
        """
        key_dict_0 = {'qrcode0': qrcode}
        key_dict_1 = {'qrcode1': qrcode}
        key_dict_2 = {'qrcode2': qrcode}
        key_dict_3 = {'qrcode3': qrcode}
        res = None
        i = 0
        for i in range(0, 4):
            res = self.WC.get_prodqrcode(
                False, *VALUES_TUPLE_PRODQRCODE,
                **locals()['key_dict_' + str(i)]
            )
            if len(res):
                break
        if not len(res):
            return 3, i, 0, 0, ''
        res_dist = res.distinct()
        sum = len(res)
        amount = self.sum_to_amount(sum, i, res_dist[0]['ppid'])

        if len(res_dist) == 2:

            return 2, i, amount, res_dist[0]['ppid'], res_dist[0]['batchno']
        elif len(res_dist) == 1:
            item = res_dist[0]
            if item['used'] == 0:
                return 0, i, amount, item['ppid'], item['batchno']
            else:
                return 1, i, amount, item['ppid'], item['batchno']
        else:
            return False

    def sum_to_amount(self, sum, i, ppid):
        """把二维码次数转位数量
        :parameter
            sum:二维码的数量
            i:第几级二维码
            ppid: 对应的批生产记录
        :return
            amount: 转换后的数量
        首先要获取ppid对应记录的扫码比例
        如果是0则 则amount=sum，否则amount=sum*没有扫码的级别数量
        """
        key_dict_pp = {'autoid': ppid}
        res = self.PC.get_producingplan(False, *VALUES_TUPLE_PP, **key_dict_pp)
        if not len(res):
            return 1
        qrtype = res[0]['qrtype']
        amount_list = (res[0]['bpamount'], res[0]['mpamount'], res[0]['spamount'])
        if qrtype == 1:
            return sum
        for key, value in enumerate('{:04b}'.format(qrtype)[::-1]):
            if value == '1':
                break
            elif value == '0':
                sum *= amount_list[2-key]
        return sum



    def add_ppopqrocde(self, flag, qrcode, detail):
        with transaction.atomic():
            p1 = transaction.savepoint()

            WarehouseModel.update_ppopqrcode(**detail)
            key_dict = {
                globals()['QRCODE_KIND'][flag]: qrcode
            }
            values = {'used': 1}
            self.WC.update_prodqrcode(key_dict, **values)

    def drop_ppopqrocde(self, flag, qrcode, autoid=None, **kwargs):
        with transaction.atomic():
            p1 = transaction.savepoint()

            WarehouseModel.delete_ppopqrcode(autoid, **kwargs)
            key_dict = {
                globals()['QRCODE_KIND'][flag]: qrcode
            }
            values = {'used': 0}
            self.WC.update_prodqrcode(key_dict, **values)

    def apply_productputoutpaper(self, autoid, snid=None, *args, **kwargs):
        with transaction.atomic():
            p1 = transaction.savepoint()
            WarehouseModel.update_productputoutpaper(autoid, *args, **kwargs)
            if snid is not None:
                key_dict_sn = {
                    'status': 3,
                    'deliverid': user.user_id,
                    'delivername': user.user_name
                }
                self.SLC.update_salenotes(snid, **key_dict_sn)
            key_dict = {
                'ppopid': autoid
            }
            qrcode_list = WarehouseModel.get_ppopqrcode(
                False, *VALUES_TUPLE_PPOPRCODE, **key_dict
            ).order_by('ppid')
            no_enough_list = []
            # 大中小包装得数量
            for item in qrcode_list:
                flag = item['flag']
                amount = item['amount']
                ppid = item['ppid']

                if flag == 0:
                    key_dict_rep = {
                        'pisource': 0,
                        'ppid': ppid
                    }
                    rep_list = WarehouseModel.get_productrepository(
                        **key_dict_rep
                    )
                    for rep_item in rep_list:
                        if rep_item.stockamount - amount >= 0:
                            rep_item.stockamount -= amount
                            amount = 0
                            rep_item.save()
                            break
                        else:
                            amount -= rep_item.stockamount
                            rep_item.stockamount = 0
                            rep_item.save()
                        print(rep_item.stockamount)
                    if amount > 0:
                        no_enough_list.append((0, ppid))

                elif flag == 1:
                    key_dict_rep = {
                        'pisource': 1,
                        'ppid': ppid
                    }
                    # 优先比较零头的数量
                    rep_list = WarehouseModel.get_productrepository(
                        **key_dict_rep
                    )
                    for rep_item in rep_list:
                        if rep_item.stockamount - amount >= 0:
                            rep_item.stockamount -= amount
                            amount = 0
                            rep_item.save()
                            break
                        else:
                            amount -= rep_item.stockamount
                            rep_item.stockamount = 0
                            rep_item.save()
                    if amount > 0:
                        key_dict_rep = {
                            'pisource': 2,
                            'hxid': ppid
                        }
                        # 优先比较零头的数量
                        rep_list = WarehouseModel.get_productrepository(
                            **key_dict_rep
                        )
                        for rep_item in rep_list:
                            # 剩余数量和合箱剩余数量都是足够
                            if rep_item.stockamount - amount >= 0 and \
                                    rep_item.hxstockamount - amount >= 0:

                                rep_item.stockamount -= amount
                                rep_item.hxstockamount -= amount
                                amount = 0
                                rep_item.save()
                                break
                            else:
                                amount -= rep_item.hxstockamount
                                rep_item.hxstockamount = 0
                                rep_item.save()
                        if amount > 0:
                            no_enough_list.append((1,ppid))
                elif flag == 2:
                    key_dict_rep = {
                        'pisource': 2,
                        'ppid': ppid
                    }
                    rep_list = WarehouseModel.get_productrepository(
                        **key_dict_rep
                    )
                    for rep_item in rep_list:
                        # 剩余总数-合箱数量=本批的数量
                        if rep_item.stockamount - rep_item.hxstockamount - \
                                amount >= 0:
                            rep_item.stockamount -= amount
                            amount = 0
                            rep_item.save()
                            break
                        else:
                            amount -= (rep_item.stockamount - \
                                      rep_item.hxstockamount)
                            rep_item.stockamount = rep_item.hxstockamount
                            rep_item.save()
                    if amount > 0:
                        no_enough_list.append((2, ppid))

            if len(no_enough_list):
                transaction.savepoint_rollback(p1)
                return "no enough", no_enough_list
            else:
                return 'OK'


QRCODE_KIND = ('qrcode0', 'qrcode1', 'qrcode2', 'qrcode3')
VALUES_TUPLE_PPLIST = (
    'stuffid', 'stuffname', 'stufftype', 'spec', 'package', 'unit', 'amount',
    'arrivedamount', 'expireddays'
)

VALUES_TUPLE_PRODQRCODE = ('ppid', 'batchno', 'used')
VALUES_TUPLE_PPOPRCODE = ('ppid', 'flag', 'amount')
VALUES_TUPLE_PP = ('bpamount', 'mpamount', 'spamount', 'qrtype')
