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