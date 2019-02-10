
# coding: utf-8

# ### 네이버 영화 평점 랭킹 데이터 수집 및 분석
# 
# - 접속 주소
# > - https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=cnt&tg=0&date=19980601
# > - 맨뒤에 인자 data값을 부여하면 2005.02.07 ~ 당일 전날 수집가능.
# > - 최초에는 누락분 수집하고
# > - 운영중에는 매일 1회씩 전달 데이터를 수집하게 스케쥴링
# 

# In[1]:


from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd


# In[12]:


domain = 'https://movie.naver.com/movie/sdb/rank/rmovie.nhn'
param = '?sel=cur&date=20181010'
page = urlopen(domain + param)
soup = BeautifulSoup(page, 'html.parser')
soup


# In[13]:


# 당일 영화(현재 상영중인)에 대한 평점 획득
#1. 당일 영화 목록 획득
soup.findAll('div', class_='tit5')


# In[20]:


# 한 세트 확인
#print(soup.findAll('div',class_='tit5')[0])
#print('영화제목: [%s]' % soup.findAll('div',class_='tit5')[0].text.strip())
print('영화제목: [%s]' % soup.findAll('div',class_='tit5')[0].a.string)


# In[17]:


# 평점 세트 획득
# 개수가 동일하므로 순서대로 수집해도 상관 없다.
# 가급적이면 돌면서 세트단위를 획득하는데 보다 안정적이다.
print(len(soup.findAll('td', 'point')),len(soup.findAll('div','tit5')))


# In[30]:


#영화 제목만 배열에 모으시오
title_list=[element.text.strip() for element in soup.findAll('div',class_='tit5')]    
title_list=[element.a.string() for element in soup.findAll('div',class_='tit5')]    


# In[31]:


title_list


# In[38]:


#영화 평점만 배열에 모으시오
point_list = [element.text for element in soup.findAll('td', 'point')]


# In[39]:


point_list


# In[41]:


# 수집하고자 하는 날짜의 연속 데이터 
pd.date_range('2018-6-1',periods=132, freq='D')

