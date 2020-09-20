# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# class MyClass:
#
#     var = "안녕하세요"
#
#     def sayHello(self):
#         var = "안녕해야죠"
#         print(self.var)
#         print(var)
#
#
# if __name__ == '__main__':
#     obj = MyClass()
#     print(obj.var)
#     print(MyClass.var)
#     print(obj.sayHello())

from pandas import Series, DataFrame
from datetime import datetime as dt
import calendar

# kakao = Series([92600, 92400, 92100, 94300, 92300], index=['2016-02-19',
#                                                             '2016-02-20',
#                                                             '2016-02-21',
#                                                             '2016-02-22',
#                                                             '2016-02-23'])
# # print(kakao)
# for closing_price in kakao.values:
#     print(closing_price)

# df = DataFrame({'KOSPI': [1915, 1961, 2026, 2467, 2041],
#                    'KOSDAQ': [542, 682, 631, 798, 675]},
#                   index=[2014, 2015, 2016, 2017, 2018])
#
# print(df.loc[2014])

print(dt.now())
print(calendar.monthrange(2020, 9))
