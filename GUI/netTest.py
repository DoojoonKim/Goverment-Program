# 프로그램이 서버와 통신하는 파트
# 아무래도 미드웨어 

import requests

url = 'http://164.125.66.70:5000/loginEx'
res = requests.post(url, data={'uid':'1','upw':'1'})
resJon = res.json()
if resJon['id']==-1:
    print('로그인 실패')
else:
    print('로그인 성공',resJon['name']+'님 반갑습니다')
    print(resJon)