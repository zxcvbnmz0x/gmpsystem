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
import operator, decimal
from functools import reduce

try:
    a = decimal.Decimal()
    b = decimal.Decimal('a')
    c = decimal.Decimal(3)
except decimal.InvalidOperation:
    b = 'a'
    c = 3
print(a,b,c)
s=256*10+128*20+64*30+32*40+16*50+8*60+4*70+2*80+90
b=(2+4+8+16+32+64+128+256+512)*6
print('sum=',s/40*4000)