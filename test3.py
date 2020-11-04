from PyQt5 .QtGui import QIntValidator,QDoubleValidator,QRegExpValidator
from PyQt5.QtCore import QRegExp

def set_validator():
    intValidator = QIntValidator()
    intValidator.setRange(0,90)

    doubleValitor = QDoubleValidator()
    doubleValitor.setRange(-360,360)
    doubleValitor.setDecimals(2)
    doubleValitor.setNotation(QDoubleValidator.StandardNotation)

    reg = QRegExp('[a-z0-9]+$')
    validator = QRegExpValidator()
    validator.setRegExp(reg)


@staticmethod
def get_data(table_str, err_msg=None, display_flag=False, *args, **kwargs):
    try:
        table = globals()[table_str]
    except KeyError:
        return False
    flat = True if len(args) == 1 else False
    try:
        res = table.objects.filter(**kwargs)
        if len(args):
            if display_flag:
                return res.values_list(*args, flat=flat)
            else:
                return res.values(*args)
        else:
            return res
    except Exception as e:
        SaveExcept(e, err_msg, *args, **kwargs)

@staticmethod
def update_data(table_str, err_msg=None, condition={}, *args, **kwargs):
    try:
        table = globals()[table_str]
    except KeyError:
        return False
    try:
        if len(args):
            return table.objects.filter(autoid__in=args).update(**kwargs)
        elif len(condition):
            return table.objects.filter(**condition).update(**kwargs)
        else:
            return table.objects.create(**kwargs)
    except Exception as e:
        SaveExcept(e, err_msg, *args, **kwargs)

@staticmethod
def delete_data(table_str, err_msg=None, condition={}, *args, **kwargs):
    try:
        table = globals()[table_str]
    except KeyError:
        return False
    try:
        if len(args):
            return table.objects.filter(autoid__in=args).delete()
        elif len(condition):
            return table.objects.filter(**condition).delete()
        else:
            return table.objects.filter(**kwargs).delete()
    except Exception as e:
        SaveExcept(e, err_msg, *args, **kwargs)


from db.models import Productrepository, Producingplan, Ppopqrcode, Prodqrcode, Selfdefinedformat, Eqnormaldocuments
from django.db.models import Sum
key_dict = {'ppopid':31}
VALUES_TUPLE_PROD = (
    'ppid', 'batchno', 'used'
)
# res = Prodqrcode.objects.filter(qrcode1='10').values(*VALUES_TUPLE_PROD).distinct()
#
# print(res)
# print(res.values('used'))
#
import operator, decimal
from functools import reduce
from django.shortcuts import _get_queryset
from PyQt5.QtCore import QDateTime
from django.db.models import Q, F

s = Selfdefinedformat.objects.values('format').filter(autoid=2943)
newgen = Eqnormaldocuments.objects.create(formname="测试表")
print(newgen)
b = newgen.favor(*s)
print(b.query)


