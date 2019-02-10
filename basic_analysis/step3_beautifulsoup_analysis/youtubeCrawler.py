from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options


# 브라우저 가동(리눅스용)
chrome_options = Options()
chrome_options.add_argument('--headless') # gui가 없다
chrome_options.add_argument('--window-size=1920x1080')

# 기본 접속
driver = wd.Chrome('./data/chromedriver')
filters = {'hour':'EgQIARAB', # 지난 한시간
          'today':'EgQIAhAB', # 오늘
          'week':'EgQIAxAB',  # 이번주
          'month':'EgQIBBAB',  # 이번달
          'year':'EgQIBRAB'}  # 올해
word = 'bts'
url = 'https://www.youtube.com/results?search_query={word}&sp={date}'.format(word=word,date=filters['today'])

driver.get(url)

def getVideoCount():
    return len(driver.find_elements_by_css_selector('ytd-video-renderer'))
getVideoCount()


# 브라우저 종료
driver.close() 
driver.quit()
# 파이썬 프로그램 종료
import sys
sys.exit(0)