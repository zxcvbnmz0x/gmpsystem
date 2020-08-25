# -*- coding: utf-8 -*-
from product.modules.editproducingplanmodule import EditProducingplan


# 生产指令页面
# flag:为标记是从哪个位置打开
#       0为生产指令
#       1为生产车间
class EditProducingplan(EditProducingplan):
    def __init__(self, parent=None, autoid=None):
        super().__init__(parent, autoid)