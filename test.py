class a():
    def __init__(self):
        print("我是a")
    def show(self):
        print("show a")

if __name__ == '__main__':
    d = {
        "半成品":a
    }
    s = "半成品"
    if s in d:
        detail = d[s]()
        detail.show()