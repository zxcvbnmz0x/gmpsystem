
import os
import sys

import django


# 获取当前文件的目录
pwd = os.path.dirname(os.path.realpath(__file__))
#print(pwd)
# 获取项目名的目录(因为我的当前文件是在项目名下的文件夹下的文件.所以是../)
sys.path.append(pwd + "../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
# 初始化django
django.setup()
