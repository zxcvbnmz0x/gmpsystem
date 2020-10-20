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

from db.models import Productrepository, Producingplan
from django.db.models import Sum
res = Productrepository.objects.filter(ppid=77)
select={
                'prodid': 'prodid', 'prodname': 'prodname', 'spec': 'spec',
                'commonname': 'commonname', 'batchno': 'batchno',
                'package': 'package', 'basicunit': 'basicunit',
                'makedate': 'makedate', 'expirdedates': 'expirdedates'
            }
print(type(select))
print(res)

