# 디비에 로그 저장 => 학습 데이터로 재사용 -> 모델 업그레이드
# 파파고 연동해서 번역 제공(10분 안쪽)
import requests

url='https://openapi.naver.com/v1/papago/n2mt'
headers={
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
# 'X-Naver-Client-Id':'pXyR6yM6ywVjGZuZxvaT',
# 'X-Naver-Client-Secret':'jiY8Mso0_2'
'X-Naver-Client-Id':'5ai5c2fVYyeetmoq6Zd3',
'X-Naver-Client-Secret':'np5H9hPun5'        
}
data={
    'source':'en',
    'target':'ko',
    'text':'you are good student'
}
res = requests.post(url, headers=headers, data=data)
print(res.json())