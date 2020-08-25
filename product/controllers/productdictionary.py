from PyQt5 import QtCore, QtGui, QtWidgets

from stuff.controllers.stuffdetail import StuffDetail

from stuff.models.stuffmodel import StuffModel

from product.modules.productdictionarymodule import ProductDictionaryModule

from lib.utils.authority import Authority


class ProductDictionary(ProductDictionaryModule):
    def __init__(self, parent=None):
        super().__init__(parent)
