##### 문장 유사도 분석
# 패키지 불러오기
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

### 몇가지로 테스트
## 1. 영어 분석기
## 2. 트위터 분석기
contents = ['짱구랑 놀러가고 싶지만 바쁜데 어떻하죠?',
           '짱구는 공원에서 산책하고 노는 것을 싫어해요',
           '짱구는 공원에서 노는 것도 싫어해요. 이상해요',
           '먼 곳으로 여행을 떠나고 싶은데 너무 바빠서 그러질 못하고 있어요.']
### 데이터를 학습 가능하게끔 정제 한다.
vectorizer = CountVectorizer()

### 데이터 학습 시킨다.
### 데이터 정제
### 판단 하고자 하는 데이터를 넣는다.


#%%from urllib.request import urlopen
import urllib
import time
from bs4 import BeautifulSoup
from tqdm import tqdm_notebook
keyword = 'bts'
# 총 수집된 문장 덩어리를 담는 그릇
news_texts = []
for n in tqdm_notebook(range(1, 2000 ,10)):
    start = n # 11 ,21 ~
    target_url = 'https://search.naver.com/search.naver?&where=news&query={keyword}&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=10&start={start}&refresh_start=0'
    url = target_url.format(keyword=urllib.parse.quote(keyword), start = start)

    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    #실제 요청
    response = urllib.request.urlopen(req).read() #urlopen(url)
    soup = BeautifulSoup(response, 'html.parser')
    # 수집 데이터(+ or extend())
    news_texts += [parser.text for parser in soup.find_all('dl')]
    time.sleep(0.2)
#%%
# gensim을 이용한 word2vec 단어 유사도 분석


    
    