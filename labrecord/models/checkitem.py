import traceback

from db.models import Checkitems


class CheckItem(object):
    def __init__(self):
        super().__init__()

    # 根据物料/产品编号查询记录
    def get_checkitems(self, stuffid, itemtype):
        try:
            return Checkitems.objects.filter(
                stuffid=stuffid, itemtype=itemtype
            ).order_by('seqid')
        except Exception as e:
            print('repr(e):\t', repr(e))
            return False

    # 根据autoid查询记录
    def get_checkitem(self, autoid):
        try:
            return Checkitems.objects.get(autoid=autoid)
        except Exception as e:
            print('repr(e):\t', repr(e))
            return False

    def update_check_item(self, autoid=None, **detail):
        try:
            if autoid is None:
                return Checkitems.objects.create(**detail)
            else:
                return Checkitems.objects.filter(autoid=autoid).update(**detail)
        except Exception as e:
            print(repr(e))
            traceback.print_exc()

    def delete_check_item(self, autoid):
        try:
            return Checkitems.objects.filter(autoid__in=autoid).delete()
        except Exception as e:
            print(repr(e))
