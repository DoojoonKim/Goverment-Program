#%%
# 모듈 불러오기 
from wordcloud import WordCloud, STOPWORDS
import numpy as np 
from PIL import Image
import sys
import os
import matplotlib.pyplot as plt
#%% 선언부 불용어 사전 같은 경우 
# os.getcwd()
mask = Image.open('./data/alice_mask.png')
mask = np.array(mask)
stopwords = STOPWORDS

# stopwords.union #union 왜 안먹힘?
stopwords

text = open('./data/alice.txt').read()
print(text)
# wordcloud 설정
#%% 설정
wc = WordCloud(mask=mask,background_color ='white', max_words=1500, stopwords=stopwords )
#%% wordcloud 그림 그리기
% matplotlib inline
# text 상대빈도 생성
result = wc.generate(text)
type(result)
plt.figure(figsize=(20,10))
plt.show(result)  # 안나타남
plt.imshow(result)  # image show 




