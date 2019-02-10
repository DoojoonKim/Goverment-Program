# step4_learning.py

# pipeline은 인공신경망 여러 개를 붙여주는 역할.
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle
from time import time
import pandas as pd
from step3_word_tokenizer import tokenizer, tokenizer_porter, step3_word_tokenizer


def step4_learning():
    # csv 파일에서 데이터를 읽어온다.
    df = pd.read_csv('./data/refined_movie_review.csv')
    # 테스트, 학습데이터로 나눈다.
    X_train = df.loc[:35000-1, 'review'].values
    y_train = df.loc[:35000-1, 'sentiment'].values

    X_test = df.loc[35000:50000, 'review'].values
    y_test = df.loc[35000:50000, 'sentiment'].values

    # print(len(X_train), len(X_test))

    # 단어장을 만들어주는 객체
    tfidf = TfidfVectorizer(lowercase=False, tokenizer=tokenizer_porter)
    # 데이터를 학습하기 위한 객체
    logistic = LogisticRegression(C=10.0, penalty='l2', random_state=0)
    # 파이프 라인 설정
    pipeline = Pipeline([('vect', tfidf), ('clf', logistic)])

    # 학습한다.
    stime = time()
    print('학습 시작')
    pipeline.fit(X_train, y_train)
    print('학습 종료')
    print('총 학습시간 : %d' % (time()-stime))

    # 테스트
    y_pred = pipeline.predict(X_test)
    print("정확도 : %.3f" % accuracy_score(y_test, y_pred))

    # 학습이 완료된 객체를 저장한다.
    with open('./data/pipe.dat', 'wb') as fp:
        pickle.dump(pipeline, fp)