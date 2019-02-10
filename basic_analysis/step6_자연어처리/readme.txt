[[자연어처리]]

1. 개요
    - 한글 자연어 처리를 파이썬으로 진행
    - konlpy 모듈이 필수가 되었음.
    - www.lucypark.kr
    - https://konlpy-ko.readthedocs.io/ko/v0.4.3/
    - 모듈
    > 꼬꼬마, 한나눔, 트위터, 등등 형태소 분석기 제공
    > 자연어 처리에 필요한 사전, 말뭉치 ,도구 등을 제공
    > 쉽다.
    
2. 설치
   - 반드시 순서대로 진행할것
    > pip install konlpy
    > visual c++ build tools
    > https://www.microsoft.com/ko-kr/download/confirmation.aspx?id=48159
    -jdk 설치 (java.sun.com)
    > Top Downloads > java se
    > jdk 8.xx > windows x64 >  jdk
    > 환경변수 설정 : (윈)JAVA_HOME='jdk 경로'
                      (맥)export JAVA_HOME = $(경로)
   - jpypel 설치
    > python으로 하여금 자바의 라이브러리를 사용할 수 있게 처리하는 모듈
    > 자신이 마치 자바인듯
    > jdk 버전, 주피터 경로에 한글 주의, pc이름 한글 주의
    > conda install -c conda-forge jpype1
   - 데이터를 다분 받음
    > python
    > import nltk
    > nltk.downlad()
    -all 선택 후 download
    + 네트워크 속도에 따라 불안정하게 다운로드 될 수 있다.
    + 필요하면 재시도
    >설치된 위치
    +C:/Users/사용자계정/AppData/Roaming/nltk_data:
    +D:\nltk_data:1.14GB
   - Raw 데이터 전처리 및 백터화 처리
   > pip install wordcloud
   > pip install gensim
    