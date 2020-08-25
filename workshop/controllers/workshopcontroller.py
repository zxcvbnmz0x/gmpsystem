# -*- coding: utf-8 -*-
from workshop.modules.producingmodule import ProducingModule


# 生产指令页面
# flag:为标记是从哪个位置打开
#       0为生产指令
#       1为生产车间
class WorkshopController(ProducingModule):
    def __init__(self, autoid, parent=None):
        super().__init__(autoid, parent)
