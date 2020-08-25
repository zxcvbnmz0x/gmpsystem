from PyQt5 import QtCore, QtGui, QtWidgets

from stuff.controllers.stuffdetail import StuffDetail

from stuff.models.stuffmodel import StuffModel

from stuff.modules.stuffdictionarymodule import StuffDictionaryModule

from lib.utils.authority import Authority


class StuffDictionary(StuffDictionaryModule):
    def __init__(self, parent=None):
        super().__init__(parent)
