# # 엑셀에서 데이타 추출
# import pandas as pd
# krx_list = pd.read_html('C:/Project/Investment/dra_investar/data/상장법인목록.xls')
# # krx_list[0].종목코드 = krx_list[0].종목코드.map('{:06d}'.format)
# # print(krx_list[0])
#
# # URL에서 직접 데이타 추출
# df = pd.read_html('https://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType13')[0]
# df['종목코드'] = df['종목코드'].map('{:06d}'.format)
# df = df.sort_values(by='종목코드')
# print(df)

# 네이버에서 시세 조회 (beautiful soup4 사용 - parse는 lxml)
import pandas as pd
from bs4 import BeautifulSoup as Bs
from urllib.request import urlopen

url = 'https://finance.naver.com/item/sise_day.nhn?code=068270&page=1'
with urlopen(url) as doc:
    html = Bs(doc, 'lxml')
    pgrr = html.find('td', class_='pgRR')
    # print(pgrr.a['href'])
    # print(pgrr.text)    # 태그를 제외하고 텍스트 부분만 구할때
    s = str(pgrr.a['href']).split('=')
    last_page = s[-1]
    print(last_page)    # 마지막 페이지 구하기

df = pd.DataFrame()
sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=068270'

for page in range(1, int(last_page)+1):
    page_url = '{}&page={}'.format(sise_url, page)  # {}에 sise_url과 page번호 맵핑해서 url완성
    df = df.append(pd.read_html(page_url, header=0)[0])  # read_hrml은 데이타프레임을 가진 리스트 리턴

df = df.dropna()    # 값이 없는 행은 제거
print(df)