import re

class Student():
    def __init__(self,stid):
        if None == re.match('20((1(?=[4-9])|(2(?=[0-4])))(?=\d1)|(1(?=[2-9])|(2(?=[0-4])))(?=\d2))\d(1(?=[1-2])|2(?=[1-5]))\d\d{3}',stid):
            self.id = None
        else:
            self.id = stid
        self.stNum = None
        self.grade = None
        self.isunder = None
        self.major = None
        self.parseId()

    def parseId(self):
        if not self.id: return None
        self.grade = int(self.id[2:4])
        self.isunder = self.id[4]=="1"
        self.major = int(self.id[5])
        self.stNum = self.id[6:]
        print(self.grade, self.isunder, self.major, self.stNum)

if __name__ == '__main__':
    s = Student('202311109')