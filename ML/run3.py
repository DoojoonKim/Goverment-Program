# flask 모듈관련
from flask import Flask, render_template, request, jsonify 
# 머신러닝 모듈
from sklearn.externals import joblib
# 기타 
import os
# 정규식
import re
# 데이터 베이스
import pymysql as my

def loadMLModel():
  with conn.cursor() as cursor:
    sql = '''
    select version, fname from tbl_model_list 
    where version=(select version from tbl_ml_version where platform='web');
    '''
    cursor.execute( sql )
    row = cursor.fetchone()
    # row이 None일때 조치 사항 추가
    print( row )
  model_path = './ml/model/%s/%s' % (row['version'], row['fname'])
  return joblib.load(model_path)

# 학습데이터 로드
# model_path = './data/lang/lang.model'
# svm.SVC() 객체이면서 학습을 완료한 모델 객체
#clf        = loadMLModel() #joblib.load(model_path)
# 데이터베이스 접속
conn       = my.connect(
                host     ='127.0.0.1',
                user     ='root',
                password ='root',
                db       ='pythondb',
                charset  ='utf8',
                cursorclass=my.cursors.DictCursor
                )
# flask
app = Flask(__name__)

# 데이터 베이스 해제
def close():
  if conn:conn.close()

# API 서비스 
@app.route('/predict', methods=['POST'])
def predictAPI():
  ori_txt = request.form.get('text')
  pre     = predict( detect_file_dataEx2( ori_txt ) )
  cnt     = insertLog( ori_txt, pre['code'] )
  return jsonify( pre )

# 홈페이지
@app.route('/', methods=['GET', 'POST'])
def home():
  if request.method == 'GET':
    return render_template('index.html')
  else: # POST
    # [[ 판정  ]]
    # 전송된 데이터를 획득
    ori_txt = request.form.get('text')
    print( ori_txt )
    # 데이터 전처리 => 예측을 할수 있는데이터형태로 가공
    tmp = detect_file_dataEx2( ori_txt )
    # 예측
    langCode = predict( tmp )
    # 디비에 로그 저장 -> 학습데이터로 재사용 -> 검증후 -> 모델 업그레이드
    # insertLog()
    cnt = insertLog( ori_txt, langCode['code'] )
    if cnt:print('로그 저장 완료')
    # 파파고 연동해서 번역 제공(10분안쪽) 
    import requests as req
    url     = 'https://openapi.naver.com/v1/papago/n2mt'
    headers = {
      'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
      'X-Naver-Client-Id':'pXyR6yM6ywVjGZuZxvaT',
      'X-Naver-Client-Secret':'jiY8Mso0_2'
    }
    data    = {
      'source':langCode['code'],
      'target':'ko',
      'text':ori_txt
    }
    res     = req.post(url, headers=headers, data=data)
    # 응답 구성
    return '''
      <div>판독한 언어 : [%s]<div>
      <div>번역한 내용 : %s<div>
      <button onclick='javascript:history.back();'>뒤로</button>
    ''' % (langCode['name'], res.json()['message']['result']['translatedText'] )

def predict( src ):
  # 모델 생성
  clf  = loadMLModel()
  # 예측
  res  = clf.predict( src )
  # 결과 리턴
  return selectLang( res[0] )

def insertLog( txt, code ):
  with conn.cursor() as cursor:
    sql = 'insert into tbl_lang_log (`text`, code) values ( %s, %s );'
    cursor.execute( sql, (txt, code) )    
  # 디비 반영
  conn.commit()
  # 영향받은 row의 수
  return conn.affected_rows()

# 예측값을 넣어서 쿼리 쳐서 언어 이름을 획득
def selectLang( code ):
  with conn.cursor() as cursor:
    sql = 'select code, name from tbl_lang where code=%s;'
    cursor.execute( sql, (code,) )
    row = cursor.fetchone()
  return row

def detect_file_dataEx2(text):    
  text          = re.compile(r'[^a-z]+').sub('', text.lower() )    
  counts        = [ 0 ] * 26
  ASCII_A_CODE  = ord('a')
  for n in text:counts[ ord(n)-ASCII_A_CODE ] += 1    
  total_count   = sum(counts)
  freqs         = [ c/total_count for c in counts ]    
  freqs_tmp     = []
  freqs_tmp.append( freqs )
  return freqs_tmp

def detect_file_dataEx(text):
  # 사용자가 입력한 텍스트를 소문자로
  text   = text.lower()
  # 알파벳 소문자만 두고 나머지는 모두 제거
  text   = re.compile(r'[^a-z]+').sub('',text)

  counts = [ 0 ] * 26
  ASCII_A_CODE  = ord('a')
  for n in text:counts[ ord(n)-ASCII_A_CODE ] += 1
  # 빈도를 0~1사이로 정규화 => 총 발생 빈도 대비 알파벳별 발생 빈도
  total_count   = sum(counts)
  freqs  = [ c/total_count for c in counts ]    

  freqs_tmp     = []
  freqs_tmp.append( freqs )
  # 예측시에는 [ [0.1223, 0.1221 , ...]  ] 이것만 있으면 된다
  return freqs_tmp

def makeDir(path):
  check_step1_path = path
  if not os.path.exists( check_step1_path ):#해당 경로 없음(폴더없음)
    os.mkdir(check_step1_path)

# modelMake.py에서 model 파일을 업로드하면 
# 디스크상에 저장, 디비에 기록하고 응답하는 API
@app.route('/upload', methods=['POST'])
def upload():
  # 전달된 데이터 획득 ()
  version  = request.form.get('version')
  fname    = request.form.get('fname')
  comment  = request.form.get('comment')
  score    = request.form.get('score')
  fileData = request.files['fileData']
  # 데이터 검증 생략 (다 잘왔다 가정)  
  # 디스크에 저장 (버전 폴더생성) ; ml\model 여기 밑으로 저장한다
  # sub1 : 해당 버전으로 폴더가 있는지 없으면 신규 생성
  makeDir( '.\\ml\\model\\%s' % version )
  # sub2 : 업로드된 파일 저장
  check_step2_path = '.\\ml\\model\\%s\\%s' % (version, fileData.filename)
  # 파일저장
  fileData.save( check_step2_path )
  # 디비에 신규 모델 정보 입력
  with conn.cursor() as cursor:
    sql = 'insert into tbl_model_list (version,fname,comment,score) values (%s,%s,%s,%s);'
    cursor.execute( sql, (version,fname,comment,score) )    
  # 디비 반영
  conn.commit()
  # 응답 => ok/fail
  # 영향받은 row의 수 => 응답
  if conn.affected_rows():
    return jsonify( {'code':'ok'} )
  else:
    return jsonify( {'code':'fail'} )
  

# 서버 구동
if __name__ == '__main__':
  app.run(debug=True)

