import decimal
import re

from math import log, log10, log2, sin, cos, tan, e, factorial, floor, ceil, \
    pow, sqrt, pi


# 四舍六入五成双
# 解决浮点数不精确的问题
# ≤4 时舍去，"六"是指≥6时进上，
# "五"指的是根据5后面的数字来定，当5后有数时，舍5入1；
# 当5后无有效数字时，需要分两种情况来讲：
#   （1）5前为奇数，舍5入1；
#   （2）5前为偶数，舍5不进（0是偶数）。
def rnd(p_str, p_int: int = 1):
    if type(p_str) != 'decimal.Decimal':
        return round(decimal.Decimal(str(p_str)), p_int)
    else:
        return round(p_str, p_int)

# 开根号
# num:开多少次方，默认为2次方
def pown(p_int: int, num=2):
    if num == 2:
        return sqrt(p_int)
    else:
        return pow(p_int, 1 / num)


# 取整
# num = 1   向上取整
# num = -1  向下取整
def ceilf(p_int: int, num=0):
    if num == 1:
        return ceil(p_int)
    elif num == -1:
        return floor(p_int)
    else:
        return p_int


def sumf(*args):
    count = decimal.Decimal('0')
    for item in args:
        try:
            count += decimal.Decimal(str(item))
        except decimal.InvalidOperation:
            pass
    return count


def avgf(*args):
    count = decimal.Decimal('0')
    i = 0
    for item in args:
        try:
            count += decimal.Decimal(str(item))
            i += 1
        except decimal.InvalidOperation:
            pass
    return count/i


def evalenv(self):
    env = {
        "self": self,
        "abs": abs,
        "rnd": rnd,
        "log": log,
        "log10": log10,
        "log2": log2,
        "sin": sin,
        "cos": cos,
        "mathpi": pi,
        "pown": pown,
        "ceilf": ceilf,
        "tan": tan,
        "mathe": e,
        "factorial": factorial,
        "sum": sumf,
        "avg": avgf
    }
    return env


