# -*- coding：utf-8 -*-<br>
class A(object):
    def __init__(self, xing, gender):  # ！#1
        self.namea = "aaa"  # ！#2
        self.xing = xing  # ！#3
        self.gender = gender  # ！#4

    def funca(self):
        print("function a : {}".format(self.namea))


class B(A):
    def __init__(self, xing, age, gender):  # ！#5
        super(B, self).__init__(xing, gender)  # ！#6（age处应为gender）
        self.nameb = "bbb"  # ！#7
        ##self.namea="ccc"                  #！#8
        ##self.xing = xing.upper()          #！#9
        self.age = age  # ！#10

    def funcb(self):
        print("function b : %s" % self.nameb)


b = B("lin", 22, 'nan')  # ！#11
print(b.nameb)
print(b.namea)
print(b.xing)  # ！#12
print(b.age)
print(b.gender)# ！#13
b.funcb()
b.funca()
