from PyQt5 import QtCore


def readXML(file):
    reader = QtCore.QXmlStreamReader()
    try:
        # 传入的是地址
        qfile = QtCore.QFile(file)
        # 找到文件,则设置引擎,否则向xml文件直接添加数据
        if qfile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            reader.setDevice(file)
        else:
            reader.addData(file)
        reader.readNext()
        if reader.isStartDocument():
            reader.readNext()
        # 如果没有读到文档结尾，而且没有出现错误
        while not reader.atEnd():
            if reader.isStartElement():
                if reader.name() == "GMPPaper":
                    reader.readNext()
                elif reader.name() == "Title":
                    reader.readNext()
                else:
                    reader.readNext()
            # 读取注释内容
            elif reader.isComment():
                reader.readNext()
            # 结束标签
            elif reader.isEndElement():
                reader.readNext()
            # 空格组成的字符，包括换行
            elif reader.isWhitespace():
                reader.readNext()
            # 纯文本
            elif reader.isCharacters():
                reader.readNext()
            # 如果读取过程中出现错误，那么输出错误信息
            if reader.hasError():
                print(reader.errorString())
                pass
        qfile.close()
    except :
        raise ValueError
