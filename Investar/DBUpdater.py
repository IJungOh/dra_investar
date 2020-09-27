# DBUpdater - 스텁(stub)코드 : 인터페이스는 정의되어 있으나 실제 코드가 구현되지 않은 상태의 코드
from datetime import datetime
from threading import Timer
from urllib.request import urlopen

import calendar
import json
import pandas as pd
import pymysql
from bs4 import BeautifulSoup as Bs


class DBUpdater:
    def __init__(self):
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        self.conn = pymysql.connect(host='localhost', user='root', password='admin',
                                    db='investar', charset='utf8')
        with self.conn.cursor() as curs:
            sql = """
            CREATE TABLE if NOT EXISTS company_info (
                code VARCHAR(20),
                company VARCHAR(40),
                last_update DATE,
                PRIMARY KEY (CODE)
            )
            """
            curs.execute(sql)
            sql = """
            CREATE TABLE if NOT EXISTS daily_price (
                code VARCHAR(20),
                DATE DATE,
                OPEN BIGINT(20),
                high BIGINT(20),
                low BIGINT(20),
                close BIGINT(20),
                diff BIGINT(20),
                volume BIGINT(20),
                PRIMARY KEY (CODE, DATE)
            )
            """
            curs.execute(sql)
        self.conn.commit()

        self.codes = dict()

    def __del__(self):
        """소멸자: MariaDB 연결 해제"""
        self.conn.close()

    def read_krx_code(self):
        """KRX로부터 상장법인목록 파일을 읽어와서 데이터프레임으로 반환"""
        """테스트를 위해 한종목만 생성-"""
        # url = 'https://kind.krx.co.kr/corpgeneral/corpList.do?method=' \
        #       'download&searchType=13'
        # krx = pd.read_html(url, header=0)[0]
        url = 'C:/Project/Investment/document/stock_list.xlsx'
        krx = pd.read_excel(url, sheet_name='list', header=0)
        krx = krx[['종목코드', '회사명']]
        krx = krx.rename(columns={'종목코드': 'code', '회사명': 'company'})
        krx.code = krx.code.map('{:06d}'.format)
        return krx

    def update_comp_info(self):
        """종목코드를 company_info 테이블에 업데이트한 후 딕셔러리에 저장"""
        # replace into 구문사용 oracle merge into 와 비슷함 (upsert)
        # 대상이 없으면 insert, 있으면 update

        sql = "SELECT * FROM company_info"
        df = pd.read_sql(sql, self.conn)
        for idx in range(len(df)):
            self.codes[df['code'].values[idx]] = df['company'].values[idx]
        with self.conn.cursor() as curs:
            sql = "SELECT max(last_update) FROM company_info"
            curs.execute(sql)
            rs = curs.fetchone()
            today = datetime.today().strftime('%Y-%m-%d')
            print('WooHoo' + today)

            if rs[0] == None or rs[0].strftime('%Y-%m-%d') < today:
                krx = self.read_krx_code()
                for idx in range(len(krx)):
                    code = krx.code.values[idx]
                    company = krx.company.values[idx]
                    sql = f"REPLACE INTO company_info (code, company, last_update)" \
                          f"VALUES ('{code}', '{company}', '{today}')"
                    curs.execute(sql)
                    self.codes[code] = company
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] {idx:04d} REPLACE INTO company_info " \
                          f"VALUES ({code}, {company}, {today})")

                self.conn.commit()
                print('')

    def read_naver(self, code, company, pages_to_fetch):
        """네이버 금융에서 주식 시세를 읽어서 데이터프레임으로 반환"""
        try:
            url = f"https://finance.naver.com/item/sise_day.nhn?code={code}"
            with urlopen(url) as doc:
                if doc is None:
                    return None
                html = Bs(doc, "lxml")
                pgrr = html.find("td", class_="pgRR")
                if pgrr is None:
                    return None

                s = str(pgrr.a["href"]).split('=')
                lastpage = s[-1]

            df = pd.DataFrame()
            pages = min(int(lastpage), pages_to_fetch)
            for page in range(1, pages + 1):
                pg_url = '{}&page={}'.format(url, page)
                df = df.append(pd.read_html(pg_url, header=0)[0])
                tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                print('[{}] {} ({}) : {:04d}/{:04d} pages are downloading...'.
                      format(tmnow, company, code, page, pages), end="\r")

            df = df.rename(columns={'날짜': 'date', '종가': 'close', '전일비': 'diff', '시가': 'open', '고가': 'high',
                                    '저가': 'low', '거래량': 'volume'})
            df['date'] = df['date'].replace('.', '-')
            df = df.dropna()
            # 마리아 DB에서 BIGINT로 지정한 컬럼의 데이터형을 INT로 변경
            df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[['close', 'diff', 'open', 'high',
                                                                         'low', 'volume']].astype(int)

            # 원하는 순서로 컬럼순서 변경
            df = df[['date', 'open', 'high', 'low', 'close', 'diff', 'volume']]

        except Exception as e:
            print('Exception occured :', str(e))
            return None
        return df

    def replace_into_db(self, df, num, code, company):
        """네이버 금융에서 읽어온 주식 시세를 DB에 REPLACE"""
        with self.conn.cursor() as curs:
            for r in df.itertuples():
                sql = f"REPLACE INTO daily_price VALUES ('{code}',  " \
                      f"'{r.date}', {r.open}, {r.high}, {r.low}, {r.close}, " \
                      f"{r.diff}, {r.volume})"
                curs.execute(sql)
            self.conn.commit()
        print('[{}] #{:04d} {} ({}) : {} rows > REPLACE INTO daily_' \
              'price [OK]'.format(datetime.now().strftime('%Y-%m-%d' \
                                                          ' %H:%M'), num + 1, company, code, len(df)))

    def update_daily_price(self, pages_to_fetch):
        """KRX 상장법인의 주식 시세를 네이버로부터 읽어서 DB에 업데이트"""
        for idx, code in enumerate(self.codes):  # codes 딕셔너리에 저장된 종목 처리
            df = self.read_naver(code, self.codes[code], pages_to_fetch)
            if df is None:
                continue
            self.replace_into_db(df, idx, code, self.codes[code])

    def execute_daily(self):
        """실행 즉시 및 매일 오후 다섯시에 daily_price 테이블 업데이트"""
        # 상장법인목록 DB (company_info)에 업데이트
        self.update_comp_info()
        try:
            with open('config.json', 'r') as in_file:
                config = json.load(in_file)
                page_to_fetch = config['page_to_fetch']
        except FileNotFoundError:
            with open('config.json', 'w') as out_file:
                page_to_fetch = 100
                config = {'page_to_fetch': 1}
                json.dump(config, out_file)  # json객체를 config.json 파일에 쓰기

        self.update_daily_price(page_to_fetch)

        tmnow = datetime.now()
        # monthrange(int, int) - 연도와 월을 int형으로 전달하면 [첫째일, 마지막일] 리스트 리턴
        lastday = calendar.monthrange(tmnow.year, tmnow.month)[1]

        if tmnow.month == 12 and tmnow.day == lastday:  # 연마지막날이면,
            tmnext = tmnow.replace(year=tmnow.year + 1, month=1, day=1, hour=17, minute=0, second=0)
        elif tmnow.day == lastday:
            tmnext = tmnow.replace(month=tmnow.month + 1, day=1, hour=17, minute=0, second=0)
        else:
            tmnext = tmnow.replace(day=tmnow.day + 1, hour=17, minute=0, second=0)

        tmdiff = tmnext - tmnow
        secs = tmdiff.seconds

        t = Timer(secs, self.execute_daily)

        print("Wating for next update ({}) ...".format(tmnext.strftime('%Y-%m-%d %H:%M')))
        t.start()


if __name__ == '__main__':
    dbu = DBUpdater()
    dbu.execute_daily()
