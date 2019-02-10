from sklearn import svm
import json
from sklearn.externals import joblib
import os
#1. 학습 데이터 로딩
with open('./data/lang/full.json','r',encoding='utf8') as fp:
    d = json.load(fp)
print('>'*10, '[학습 데이터 로드 OK]')

#2. 모델 생성 및 학습

clf = svm.SVC(gamma='auto')
clf.fit(d[0]['freq'],d[0]['labels'])
print('>'*10, '[학습OK]')

# 덤프 처리 => binary data
DUMP_PATH = './data/lang/lang10.model'
joblib.dump(clf, DUMP_PATH)
print('>'*10,'[덤프처리OK]')

import requests
# 전송 정보 및 데이터
url = 'http://127.0.0.1:5000/upload'
files = {'fileData': open(DUMP_PATH,'br')}
# 세팅된 내용은 디비조회 or 파일자체정보 or 직접입력, 실제평가(?)해서 얻을 수 있다.
data = {'version':'1.0.3', 'fname':'lang10.model', 'comment':'test', 'score':'0.90'}
# 전송 처리
print('>'*10, '[업로드 데이터 준비 OK]')
requests.post(url, files=files, data=data)
print('>'*10, '[업로드 OK]')