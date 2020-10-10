from _datetime import datetime
import json
import traceback
import os


def SaveExcept(error, describe=None, data=None, *args, **kwargs):
    try:
        # 建立目录
        os.makedirs("log/error")
    except FileExistsError:
        pass
    dt = datetime.now()
    filename = dt.strftime('%Y%m%d') + ".txt"
    # 打开当天的文件，若不存在则自动创建
    f = open("log/error/" + filename, 'a')
    with f:
        f.write("\n" + dt.strftime('%Y-%m-%d %H:%M:%S') + "\n")
        f.write(repr(error) + "\n")
        traceback.print_exc(file=f)
        f.write("\n")
        if describe:
            f.write(describe + "\n")
        if data:
            try:
                f.write(str(data))
                f.write("\n")
            except Exception:
                pass
        if args:
            f.write("args="+json.dumps(args, ensure_ascii=False, cls=DateEnconding) + "\n")
        if kwargs:
            f.write("kwargs=" + json.dumps(kwargs, ensure_ascii=False, cls=DateEnconding) + "\n")
        f.write("-"*20)
        f.close()


class DateEnconding(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            print("datetime." + str(o))
            # return "datetime." + o.strftime('%Y-%m-%d %hh:%MM-%ss')
            return "datetime." + str(o)
