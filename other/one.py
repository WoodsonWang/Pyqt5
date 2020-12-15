"""
@author:Wang Xinsheng
@File:one.py
@description:...
@time:2020-10-26 10:14
"""
class Person:
    def __init__(self,name='Person'):
        self.name = name

    def p(self):
        print("你好")
class One(Person):
    pass

class Two(Person):
    print("我是Two")
    def __init__(self,name):
        super().__init__(name)
        # super().p()
        # print(super.name)

class Three(Person):
    def __init__(self,age):
        self.age = age

import os
if __name__ == '__main__':
    # p1 = One()
    # print(p1.name)
    # p2 = Two("小王")
    # print(p2.name)
    # p3 = Three(12)
    # print(p3.age)
    # size = 3774873
    # time = int(size / 1024)
    # step = 100 / time
    # sum = 0
    # print(step)
    # for i in range(time+1):
    #     sum += step
    # print(int(sum))
    # print(os.getcwd())

    # print("99"+'0000')
    file = 'D:\\codeproject\\github\\Notes\\_posts\\2020-10-31-通过githubpages搭建博客.md'
    # file = 'D:\\codeproject\\github\\Notes\\_posts\\2020-10-28-Test.md'
    # file = 'D:\\codeproject\\github\\Notes\\_posts\\2020-10-31-other其他.md'
    import chardet
    #
    # with  open(file, 'rb') as f:
    #     data = f.read()
    #
    #     print(chardet.detect(data))
    import datetime
    time = datetime.datetime.now().strftime('%Y-%m-%d')
    print(type(time))
    print(os.path.exists(file))