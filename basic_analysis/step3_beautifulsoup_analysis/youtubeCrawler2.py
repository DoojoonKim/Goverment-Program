from selenium import webdriver as wd

# 기본 접속
driver = wd.PhantomJS('./data/phantomjs')
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
driver.save_screenshot('scene001.png')
print('driver.page_source',driver.page_source)

# 브라우저 종료
driver.close() 
driver.quit()
# 파이썬 프로그램 종료
import sys
sys.exit(0)