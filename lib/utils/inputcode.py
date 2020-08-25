# -*- coding: utf-8 -*-
from pypinyin import pinyin, Style


class Inputcode(object):
    @staticmethod
    def make_inputcode(str):
        # 把人员名称拼音关联到输入码
        # 使用pypinyin，style设置为Style.FIRST_LETTER
        # 用join拼接生成的结果
        # 把结果转成大写后传递给self.inputCode
        input_name = pinyin(str, style=Style.FIRST_LETTER)
        output = []
        for key in range(len(input_name)):
            output.append(input_name[key][0])
        outputcode = ''.join(output)
        return outputcode
