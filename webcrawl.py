from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
import urllib
from urllib.parse import quote_plus
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# 필요한 정보를 입력 받기
print("=" *80)
print("네이버에서 이미지를 검색하여 수집")
print("=" *80)

query_txt = input('크롤링할 이미지의 키워드 : ')
cnt = int(input('크롤링할 건 수 : '))

f_dir = "D:\\webcrawling"
if f_dir =='':
    f_dir = "c:\\temp\\"

print("\n")

driver_path = "D:\\webcrawling\\chromedriver-win64\\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("--timeout=YOUR_TIMEOUT_VALUE")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

print("데이터 수집 중...")

# 파일을 저장할 폴더 생성
now = time.localtime()
s = '%04d-%02d-%02d-%02d-%02d-%02d' % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

os.chdir(f_dir)
os.makedirs(f_dir+s+'-'+query_txt)
os.chdir(f_dir+s+'-'+query_txt)
f_result_dir = f_dir+s+'-'+query_txt

# URL 생성
def make_url(query_txt):
    # 네이버 이미지 검색
    base_url = 'https://search.naver.com/search.naver?where=image&section=image&query='

    # CCL 상업적 이용 가능 옵션
    end_url = '&res_fr=0&res_to=0&sm=tab_opt&color=&ccl=2' \
              '&nso=so%3Ar%2Ca%3Aall%2Cp%3Aall&recent=0&datetype=0&startdate=0&enddate=0&gif=0&optStr=&nso_open=1'

    return base_url + quote_plus(query_txt) + end_url

url = make_url(query_txt)

# 크롬 드라이버를 사용하여 웹 브라우저를 실행한 후 검색
s_time = time.time()
driver.implicitly_wait(6)
driver.get(url)

# 페이지 스크롤 다운
body = driver.find_element(By.CSS_SELECTOR, 'body')
# 또는 body = driver.find_element(By.CSS_SELECTOR, 'body')

for i in range(100):  # 스크롤 횟수 지정
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)  # delay 주기

    file_no = 0
    count = 1
img_src2 = []

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
    # XPath를 사용하여 이미지를 가져옵니다.
imgs = driver.find_elements(By.CLASS_NAME, '_fe_image_tab_content_thumbnail_image')

for img in imgs:
    img_src1 = img.get_attribute('src')
    img_src2.append(img_src1)
    count += 1

for i in range(2, len(img_src2) + 1):
    try:
        urllib.request.urlretrieve(img_src2[i], str(file_no) + '.jpg')

    except TypeError:
        continue

    file_no += 1
    time.sleep(1)
    print("\n")
    print("%s번째 이미지 저장========" %file_no)
    print("\n")

    if file_no == cnt:
        break

# 요약 정보 출력
e_time = time.time()
t_time = e_time - s_time

store_cnt = file_no - 1

print("=" *70)
print("총 소요시간은 %s초" %round(t_time, 1))
print("총 저장 건수는 %s건" %file_no)
print("파일 저장 경로는 %s" %f_result_dir)
print("=" *70)

driver.close()

