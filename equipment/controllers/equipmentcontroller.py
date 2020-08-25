# -*- coding: utf-8 -*-

from equipment.models.equipmentmodel import EquipmentModel

class EquipmentController(object):

    def get_equip_run_note(self, autoid=0, olist=[], *args, **kwargs):
        eqrunnotes = EquipmentModel.get_equip_run_note(autoid, olist, *args, **kwargs)
        #return eqrunnotes
        if len(eqrunnotes):
            eqno_set = set(eqrunnotes.values_list('eqno', flat=True))
            equipments = self.get_equipment(0, [], 'eqno', 'eqname', eqno__in=eqno_set)

            for item in eqrunnotes:
                item.eqname = ''
                for eq in equipments:
                    if item.eqno == eq[0]:
                        item.eqname = eq[1]
            return eqrunnotes
        else:
            return []

    def get_equipment(self, autoid=0, olist=[], *args, **kwargs):
        return EquipmentModel.get_equipment(autoid, olist, *args, **kwargs)

    def delete_equip_run_note(self, autoid, *args, **kwargs):
        return EquipmentModel.delete_equip_run_note(autoid, *args, **kwargs)

    def insert_equip_run_note(self, autoid, *args, **kwargs):
        return EquipmentModel.insert_equip_run_note(autoid, *args, **kwargs)

    def update_equip_run_note(self, autoid, *args, **kwargs):
        return EquipmentModel.update_equip_run_note(autoid, *args, **kwargs)