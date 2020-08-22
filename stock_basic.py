# 주식 비교 및 분석
# 1. 주식 비교
# 야후 파인낸스 사용
# 필요 라이브러리는 yfinance, pandas-datareader
# 주식 시세 구하는 함수는 get_data_yahoo()
# get_data_yahoo(조회할 주식 종목 [, start=조회 기간의 시작일] [, end=조회 기간의 종료일])

from pandas_datareader import data as pdr
import yfinance as yf

yf.pdr_override()
sec = pdr.get_data_yahoo('063160.KS', start='2020-08-17')
msft = pdr.get_data_yahoo('MSFT', start='2018-05-04')

print(sec)

tmp_msft = msft.drop(columns='Volume')  # 거래량 컬럼 삭제
print(tmp_msft.tail())  # tail()은 최근 5개 데이타 출력

print(sec.index)