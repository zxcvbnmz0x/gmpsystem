# -*- coding: utf-8 -*-
from product.modules.producingplanmodule import ProducingplanModule


# 生产指令页面
# flag:为标记是从哪个位置打开
#       0为生产指令
#       1为生产车间
class Producingplan(ProducingplanModule):
    def __init__(self, parent=None, flag=0):
        super().__init__(parent, flag)

