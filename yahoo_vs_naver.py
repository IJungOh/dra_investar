# # ch05_01_YahooFinance_SEC.py
# from pandas_datareader import data as pdr
# import yfinance as yf
# from matplotlib import pyplot as plt
# # from matplotlib.pyplot as plt => 동일한 표현
#
# yf.pdr_override()
#
# df = pdr.get_data_yahoo('005930.KS', '2017-01-01')
#
# plt.figure(figsize=(9, 6))
# plt.subplot(2, 1, 1)
# plt.title('Samsung Electronics (Yahoo Finance)')
# plt.plot(df.index, df['Close'], 'c', label='Close')
# plt.plot(df.index, df['Adj Close'], 'b--', label='Adj Close')
# plt.legend(loc='best')
# plt.subplot(2, 1, 2)
# plt.bar(df.index, df['Volume'], color='g', label='Volume')
# plt.legend(loc='best')
# plt.show()

# mariaDB Connection Test
import pymysql

connection = pymysql.connect(host='localhost', port=3306, db='investar',
                             user='root', passwd='admin', autocommit=True)
cursor = connection.cursor()
cursor.execute("select version();")
result = cursor.fetchone()

print("MariaDB version : {}".format(result))

connection.close()

# ch05_02_NaverDatabase_SEC.py
# import matplotlib.pyplot as plt
# from Investar import Analyzer


