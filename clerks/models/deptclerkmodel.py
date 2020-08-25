import traceback

from db.models import Department, Clerkdept, Clerks


class DeptClerkModel(object):
    def __init__(self):
        super().__init__()

    # 获得所有人员信息
    def get_all_clerks(self, deptid="", disabled=0):
        if deptid:
            clerks_id_list = Clerkdept.objects.filter(deptid=deptid).\
                values('clerkid')
            return Clerks.objects.filter(pid__in=clerks_id_list, disabled=disabled).values\
                (
                    'pid','clerkname','sex','birthday','entranceday','edudegree',
                    'marrystatus','idno','telno','clerkid'
                )
        else:
            return Clerks.objects.filter(disabled=disabled).values\
                (
                    'pid','clerkname','sex','birthday','entranceday','edudegree',
                    'marrystatus','idno','telno','clerkid'
                )

    # 获得所有部门
    def get_all_deptment(self, *args, **kwargs):
        if args:
            return Department.objects.values(*args)
        else:
            return Department.objects.all()

    # 新建部门
    def create_deptment(self,**kwargs):
        if kwargs:
            try:
                return Department.objects.create(**kwargs)
            except Exception as e:
                print("插入部门发生错误")
                # 这个是输出错误的具体原因，这步可以不用加str，输出
                print("这里是错误的具体原因")
                # 输出 repr(e):	ZeroDivisionError('integer division or modulo by zero',)
                print('repr(e):\t', repr(e))
                # 以下两步都是输出错误的具体位置的
                print('traceback.print_exc():')
                traceback.print_exc()
        else:
            raise("参数错误")

    def update_deptment(self, dept_id, **kwargs):
        if kwargs:
            try:
                return Department.objects.filter(deptid=dept_id).update(**kwargs)
            except Exception as e:
                print("插入部门发生错误")
                # 这个是输出错误的具体原因，这步可以不用加str，输出
                print("这里是错误的具体原因")
                # 输出 repr(e):	ZeroDivisionError('integer division or modulo by zero',)
                print('repr(e):\t', repr(e))
                # 以下两步都是输出错误的具体位置的
                print('traceback.print_exc():')
                traceback.print_exc()
        else:
            raise("参数错误")

    # 删除部门
    def del_deptment(self, *args):
        print(args)
        return Department.objects.filter(deptid__in=args).delete()

    # 获得指定id和name的人员信息
    def get_clerk(self, clerkid):
        try:
            return Clerks.objects.filter(clerkid=clerkid).\
                values('pid', 'clerkname', 'inputcode', 'sex', 'birthday',
                       'marrystatus', 'nation', 'native', 'policystatus', 'idno',
                       'address', 'telno', 'entranceday', 'edudegree', 'special',
                       'schoolname', 'techtitle', 'strongsuit', 'powers'
                       )
        except Exception as e:
            print("查找人员信息发生错误")
            print('repr(e):\t', repr(e))
            traceback.print_exc()

    def get_clerks(self, pid, *args, **kwargs):
        if pid:
            kwargs.update(pid__in=pid)
        flat = True if len(args) == 1 else False
        if len(args):
            return Clerks.objects.filter(**kwargs).values_list(*args, flat=flat)
        else:
            return Clerks.objects.filter(**kwargs)

    def get_content(self, content):
        try:
            return Clerks.objects.values_list(content, flat=True).distinct()
        except Exception as e:
            print("查找人员信息发生错误")
            print('repr(e):\t', repr(e))
            traceback.print_exc()

    # 更新人员信息，需要传入更新的内容
    def update_clerk_detail(self, detail, clerkid=""):
        if clerkid:
            try:
                return Clerks.objects.filter(clerkid=clerkid).update(**detail)
            except Exception as e:
                print("更新人员信息发生错误")
                print('repr(e):\t', repr(e))
                traceback.print_exc()
        else:
            try:
                return Clerks.objects.create(**detail).distinct()
            except Exception as e:
                print("更新人员信息发生错误")
                print('repr(e):\t', repr(e))
                traceback.print_exc()
