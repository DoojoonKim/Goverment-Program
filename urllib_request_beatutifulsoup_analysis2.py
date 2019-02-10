from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import pymysql as sql
from sqlalchemy import create_engine
import pandas.io.sql as pSql

url_ori = 'https://finance.naver.com'
url = url_ori +'/marketindex/'
pageinfo = urlopen(url)
soup = BeautifulSoup(pageinfo, 'html.parser')
exchangeUrl = soup.select_one('#frame_ex1')['src']
soup.select_one('#frame_ex1')

# 환율 정보 제공 업체, 
div = soup.find('div', class_='exchange_info')
div.text[1:-1].split('\n')
# 환율 정보 제공 업체, 
div = soup.find('div',class_='exchange_info')
k = div.select_one('span.date') # select의 결과물은 list, select_one의 결과물은 element
div = soup.find('div',class_='exchange_info')
exchange_metaInfo= []
for span in div.findAll('span'):    
    if span.find('em'):
        exchange_metaInfo.append(span.find('em').get_text())
    else:       
        exchange_metaInfo.append(span.text)
exchange_metaInfo[1] = exchange_metaInfo[1].split()[0]        
date = ''.join(exchange_metaInfo[0].split()[0].split('.'))
round_= exchange_metaInfo[2]
exchange_metaInfo.append(date+"_"+round_)
res = urlopen(url_ori+ exchangeUrl)
if_soup = BeautifulSoup(res, 'html5lib')



info = list()
for tr in if_soup.select('tbody tr'):
    for td in tr.findAll('td'):       
        info.append(td.getText().strip()) 
    

arr = np.array(info).reshape(len(info)//7,7)
df = pd.DataFrame(arr)
col = ['통화명','매매기준율','사실 때','파실 때','보내실 때','받으실 때','미화환산율']
df.columns=col

df.set_index('통화명', inplace=True)

df['회차']=exchange_metaInfo[3]

# 연결
engine = create_engine('mysql+pymysql://root:root@localhost:3306/pythondb', encoding='utf-8') #http://와 유사
conn = engine.connect()
df.columns=['rate','buy','sell','send','recv','us_rate','code']
df.index.name = 'cur'
df.to_sql(name='tbl_exchange',
          con=conn,
          if_exists='append')
# # 닫기
conn.close()

#code
exchange_metaInfo
#df 생성
meta_df = pd.DataFrame(exchange_metaInfo)
#축변경
meta_df = meta_df.T
#컬럼 조정
meta_df.columns=['date','standard','round','code']

# 연결
engine = create_engine('mysql+pymysql://root:root@localhost:3306/pythondb', encoding='utf-8') #http://와 유사
conn = engine.connect()

meta_df.to_sql(name='tbl_exchcode',
              con = conn,
                if_exists = 'append',               
               index = False
              ) 

conn.close()

