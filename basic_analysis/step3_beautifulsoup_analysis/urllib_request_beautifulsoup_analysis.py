from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import pymysql as sql
from sqlalchemy import create_engine
import pandas.io.sql as pSql

class ExchangeDataCrawler:
    # 맴버 변수
    NAVER_FINANCE_URL = 'https://finance.naver.com'
    DB_CONNECTION_TEST_URL = 'mysql+pymysql://root:root@localhost:3306/pythondb'
    DB_CONNECTION_REAL_URL = 'mysql+pymysql://root:12341234@pythondb.c69gi2s1odpt.ap-northeast-2.rds.amazonaws.com:3306/pythondb'
    DB_CONNECTION_USE_URL = ''
    # 생성자
    def __init__(self, flag=None):
        if flag: # 상용(서비스용):aws 에서 데이터 적재함.
            self.DB_CONNECTION_USE_URL = self.DB_CONNECTION_REAL_URL                            
        else:  # 테스트용(개발용): 로컬 디비에서 데이터 적재함.
            self.DB_CONNECTION_USE_URL = self.DB_CONNECTION_TEST_URL
    # 맴버 함수
    # 주어진 url에서 html 덩어리를 가져온다.
    # 네이버 파이넨스 접속해서 환율 정보 획득
    def getHtmlChunk(self):
        # 네이버 파이넨스 접속 및 환율 정보 페이지 획득
        url = self.NAVER_FINANCE_URL
        pageInfo = urlopen( url + '/marketindex/')
        soup = BeautifulSoup( pageInfo,  'html.parser')
        exchangeUrl = soup.select_one('#frame_ex1')['src']
        exchangeUrl = url + exchangeUrl
        
        #환율 메타 정보 획득 작업
        div = soup.find('div', class_='exchange_info')        
        exchange_metaInfo = []
        for span in div.find_all('span'):
            if span.find('em'):
                exchange_metaInfo.append( span.find('em').get_text() )
            else:
                exchange_metaInfo.append( span.get_text() )
        
        exchange_metaInfo[1] = exchange_metaInfo[1][:len(' 기준')*-1]
        # 코드생성
        exchange_metaInfo.append('%s_%s' % (exchange_metaInfo[0].replace('.','')[:8], 
                                            exchange_metaInfo[2]) )
        # 실제 환율 정보가 들어간 iframe 내 페이지 접근.
        res = urlopen( exchangeUrl )
        if_soup = BeautifulSoup( res, 'html5lib' )
        return exchange_metaInfo, if_soup
    # soup까지 생성해서 리턴  
    # 실제 환율 정보 크롤링  
    def crawling(self):               
        exchange_metaInfo, if_soup = self.getHtmlChunk()
        info = list()
        # 환율 정보를 7의 배수로 반복되어서 리스트에 담았다.
        for tr in if_soup.select('tbody tr'):
            for td in tr.findAll('td'):
                info.append( td.getText().strip() )
        # numpy의 ndarray 생성(리스트를 입력)
        arr = np.array( info ).reshape( int(len(info)/7), 7)
        # ndarray를 재료로 dataframe으로 생성
        df = pd.DataFrame( arr )   
        df.columns = ['cur','rate','buy','sell','send','recv','us_rate']
        # cur 컬럼을 인덱스로 지정, 원본 반영
        df.set_index('cur',inplace=True)
        #컬럼 추가(코드 정보)
        df['code']=exchange_metaInfo[3]
        ####################################################
        # 디비에 수집한 데이터를 입력하세요
        self.insertCrawlingData(df,exchange_metaInfo)
        ####################################################
    def insertCrawlingData(self, df_tmp, exchange_metaInfo):
        # 디비 오픈
        engine = create_engine(self.DB_CONNECTION_USE_URL, encoding='utf8')
        conn   = engine.connect()
        # 환율 정보 입력
        df_tmp.to_sql( name='tbl_exchange',
                con=conn,
                if_exists='append' )        
        # 환율 메타 정보 입력        
        meta_df = pd.DataFrame( exchange_metaInfo )
        meta_df = meta_df.T
        meta_df.columns = ['date','standard','round','code']
        meta_df.to_sql(name = 'tbl_exchcode', con = conn, if_exists='append', index = False)
        
        conn.close()

if __name__ == '__main__':
    obj = ExchangeDataCrawler('release')#'release'
    obj.crawling()
    # 객체 해제
    del obj
    # 프로세스가 왜 살아 있지?
    # 프로세스 종료
    import sys
    print('good bye~')
    sys.exit(0)