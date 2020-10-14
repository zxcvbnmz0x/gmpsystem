import traceback

from db.models import Checkitems

from lib.utils.saveexcept import SaveExcept

class CheckItem(object):
    def __init__(self):
        super().__init__()

    # 根据物料/产品编号查询记录
    def get_checkitems(self, display_flag=False, *args, **kwargs):
        try:
            flat = True if len(args) == 1 else False
            res = Checkitems.objects.filter(**kwargs)
            if len(args):
                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取设置检验项目时出错", *args, **kwargs)

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
