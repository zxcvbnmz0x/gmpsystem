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

from db.models import Productrepository, Producingplan, Ppopqrcode, Prodqrcode
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
import operator
from functools import reduce

s=Productrepository.objects.filter(autoid=310)
b=s[0]
print(s)
b['stockamount'] -= 1
b.save()
print(b['stockamount'])