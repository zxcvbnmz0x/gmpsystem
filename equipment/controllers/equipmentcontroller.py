# -*- coding: utf-8 -*-

from equipment.models.equipmentmodel import EquipmentModel

class EquipmentController(object):

    def get_equip_run_note(self, autoid=0, olist=[], *args, **kwargs):
        eqrunnotes = EquipmentModel.get_equip_run_note(autoid, olist, *args, **kwargs)
        #return eqrunnotes
        if len(eqrunnotes):
            eqno_set = set(eqrunnotes.values_list('eqno', flat=True))
            equipments = self.get_equipment(
                False, ('eqno', 'eqname'), eqno__in=eqno_set
            )

            for item in eqrunnotes:
                item.eqname = ''
                for eq in equipments:
                    if item.eqno == eq[0]:
                        item.eqname = eq[1]
            return eqrunnotes
        else:
            return []

    def get_equipment(self, display_flag=False, *args, **kwargs):
        return EquipmentModel.get_equipment(display_flag, *args, **kwargs)

    def delete_equip_run_note(self, autoid, *args, **kwargs):
        return EquipmentModel.delete_equip_run_note(autoid, *args, **kwargs)

    def insert_equip_run_note(self, autoid, *args, **kwargs):
        return EquipmentModel.insert_equip_run_note(autoid, *args, **kwargs)

    def update_equip_run_note(self, autoid, *args, **kwargs):
        return EquipmentModel.update_equip_run_note(autoid, *args, **kwargs)

    def get_data(self, table_num: int, display_flag=False, *args, **kwargs):
        table_str = TABLE_SET[table_num][0]
        err_msg = "查询" + TABLE_SET[table_num][1]
        return EquipmentModel.get_data(
            table_str, err_msg, display_flag, *args, **kwargs
        )

    def update_data(self, table_num: int, condition={}, *args, **kwargs):
        table_str = TABLE_SET[table_num][0]
        err_msg = "更新" + TABLE_SET[table_num][1]
        return EquipmentModel.update_data(
            table_str, err_msg, condition, *args, **kwargs
        )

    def delete_data(self, table_num: int, condition={}, *args, **kwargs):
        table_str = TABLE_SET[table_num][0]
        err_msg = "删除" + TABLE_SET[table_num][1]
        return EquipmentModel.delete_data(
            table_str, err_msg, condition, *args, **kwargs
        )

TABLE_SET = [
    ('Equipments', "设备信息"),
    ('Eqrunnotes', "设备运行记录"),
    ('Eqcheck', "设备校验记录"),
    ('Eqrepairnotes', "设备维保/维修记录"),
    ('Eqaccidentnotes', "设备事故记录"),
    ('Eqnormaldocuments', "设备一般记录"),
]