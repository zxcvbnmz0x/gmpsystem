import pymysql

#from config.settings import DB_CONFIG


class DbHelper():
    def __init__(self):
        # 获取数据库配置，设置需要的信息
        dbparams = {
        'database': 'dhngmp',
        'user':'root',
        'password':'lst.123',
        'host':'127.0.0.1',
        'port':3306
    }
        self.db = pymysql.connect(**dbparams)
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    #查找符合要求的人员列表
    def checkusername(self,text):
        #检查输入是否为合法用户
        sql = "select pid,clerkname from dhngmp.clerks where clerkname like '%s'" % text

        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except:
            return "something is error"
    #检查人员密码是否正确
    def checkpassword(self,userid,password):
        sql = "select * from clerks where pid = '%s' and password = '%s'" %(userid , password)

        try:
            self.cursor.execute(sql)
            return self.cursor.fetchone()
        except:
            return "something is error"

    def deptall(self):
        sql = "select deptid,deptname,parentid from department"

        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except:
            pass


    def userall(self):
        sql = "select pid,clerkname,sex,birthday,entranceday,edudegree,marrystatus,idno,telno from clerks"

        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except:
            pass
