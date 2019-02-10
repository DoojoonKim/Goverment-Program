# step1_GetData.py
import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

def step1_Getdata() :
    # 영화 코드
    code_list = [167638, 109906]
    # 현재 크롤링 중인 영화가 첫번째 영화인지 여부
    chk = False
    # 영화의 갯수만큼 반복한다.
    for code in code_list:
        # 1단계 : 해당 영화의 평점 글 개수를 가져온다.
        site1 = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=%d&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false' % code
        res1 = requests.get(site1)
        if res1.status_code == requests.codes.ok:
            bs1 = BeautifulSoup(res1.text, 'html.parser')
            score_total = bs1.find(class_='score_total')
            ems = score_total.find_all('em')
            score_total = int(ems[1].text.replace(',', ''))

            # 페이지 수를 계산한다.
            pageCnt = score_total // 10
            if score_total % 10 > 0 :
                pageCnt += 1
            # print(pageCnt)

            # 현재 페이지 번호 셋팅 ( 천 몇페이지니까 이걸로 크롤링 불가능 ㅠㅠ)
            now_page = 1
            pageCnt = 5



        # 2단계 : 평점 글 정보와 평점을 가져온다.
            while now_page <= pageCnt :
                sleep(0.5)
                # 요청할 페이지의 주소
                site2 = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=%d&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=%d' % (code, now_page)
                res2 = requests.get(site2)
                if res2.status_code == requests.codes.ok :
                    bs2 = BeautifulSoup(res2.text, 'html.parser')

                    score_result = bs2.find(class_='score_result')
                    lis = score_result.find_all('li')
                    df = pd.DataFrame()
                    for obj in lis :
                        # 평점
                        star_score = obj.find(class_='star_score')
                        star_em = star_score.find('em')
                        star_score = int(star_em.text)

                        # 평가글
                        score_reple = obj.find(class_='score_reple')
                        reple_p = score_reple.find('p')
                        score_reple = reple_p.text

                        # print(star_score, score_reple)
                        # 데이터를 누적한다.
                        df = df.append([[score_reple, star_score]], ignore_index=True)

                    # 저장
                    if chk == False: # 첫 영화
                        df.columns = ['text','star']
                        df.to_csv('naver_star_data.csv', index=False, encoding='utf-8-sig')
                        chk = True
                    else: # 두번째 이후
                        df.to_csv('naver_star_data.csv', index=False, encoding='utf-8-sig', mode='a', header=False)
                    print('%d / %d' % (now_page, pageCnt))
                    now_page += 1
