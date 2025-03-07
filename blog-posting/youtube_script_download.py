from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import urllib.parse
import time
import datetime
import os

print (f"{datetime.datetime.now()} ||")
# 스크립트 실행 전 
today = datetime.date.today()
start_time = datetime.datetime.now()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
formatted_date, formatted_text, filter_today = today.strftime("%m/%d"), "당잠사", "&sp=EgIIAg%253D%253D"
encoded_date = urllib.parse.quote(formatted_date)
print (f"{datetime.datetime.now()} || {encoded_date}+{formatted_text}")

def get_htmlParse (): # STEP1
    print (f"{datetime.datetime.now()} || To searching the today video via Youtube")
    print (f"{datetime.datetime.now()} || Search Wording: {formatted_date}, Encoded phrase: {encoded_date}")
    html = driver.find_element(By.ID, 'title-wrapper').get_attribute('innerHTML')
    soup = BeautifulSoup(html.encode("utf-8"),'html.parser')
    find_text = soup.find_all(class_='yt-simple-endpoint style-scope ytd-video-renderer')
    elements = find_text
    for url in elements:
        today_title = url.get('title')
        today_href = url.get('href')
    print (f"{datetime.datetime.now()} || Today`s Title: {today_title}\n{datetime.datetime.now()}Link: {today_href}")

    return today_title, today_href

def get_youtubeScript (downsub_transfer_url): # STEP2
    print (f"{datetime.datetime.now()} || TXT Script downloads Link: {downsub_transfer_url}")
    driver.get (downsub_transfer_url) # 사이트 접속
    time.sleep(3)
    # driver.implicitly_wait(2)
    txt_btn = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/button[2]')
    ActionChains(driver).move_to_element(txt_btn).perform()
    driver.implicitly_wait(2)
    txt_btn.click()
    driver.implicitly_wait(2)
    time.sleep(2)
    print (f"{datetime.datetime.now()} || TXT File Download button clicked")

def make_changeFilename (): # STEP3
    print (f"{datetime.datetime.now()} || Checked the File in /Downloads forders, to change the file name")
    source_folder = '/Users/pj/Downloads/'
    files = os.listdir(source_folder)
    file_extension = ".txt"
    
    for file in files:
        if file.endswith(file_extension):
            old_path = os.path.join(source_folder, file)
            new_name = f"HK_Global_Market_{today}.txt"
            new_path = os.path.join(source_folder, new_name)
            
            os.rename(old_path, new_path) 
            print(f"{datetime.datetime.now()} || 파일명 변경 완료: {old_path}")
            print(f"{datetime.datetime.now()} || → {new_path}")
            
def make_patternFiles(): # STEP4
    print (f"{datetime.datetime.now()} || To re-writting the wording the 'HK_Global_Market.txt'")
    input_file_name = f"/Users/pj/Downloads/HK_Global_Market_{today}.txt"
    output_file_name = f"/Users/pj/Downloads/HK_Global_Market_{today}.txt"

    with open(input_file_name, 'r', encoding='utf-8') as input_file: # 입력 파일을 읽기 모드로 엽니다.
        text = input_file.read() # 파일 내용을 읽습니다.

    text = ' '.join(text.split()) # 두 개 이상의 공백과 줄 바꿈을 하나의 공백으로 대체합니다.
    text = text.replace('[음악]', '')

    with open(output_file_name, 'w', encoding='utf-8') as output_file: # 출력 파일을 쓰기 모드로 엽니다.
        output_file.write(text)
        output_file.write(f"\n{today} 당잠사 유투브 바로 보기 \n")
        output_file.write(f"https://www.youtube.com{today_href}")

    print(f"{datetime.datetime.now()} || Modified file saved such {output_file_name}")
    
    return (output_file_name)

# 유튜부에서 검색할 URL 인코딩 쿼리
youtube_search_url = f"https://www.youtube.com/results?search_query={encoded_date}+{formatted_text}+{filter_today}"
# 크롬 드라이버를 실행 하여, 해당 URL 조회 및 HTML 파싱
driver.get(youtube_search_url)
today_title, today_href = get_htmlParse()
time.sleep(1)
# downsub.com 에 접속하여 조회할 youtube 링크 생성
downsub_transfer_url = f'https://downsub.com/?url=https://www.youtube.com{today_href}'
get_youtubeScript(downsub_transfer_url)
driver.implicitly_wait(1)
time.sleep (1)
# 다운로드 받은 파일 확인 후 파일명을 "HK_Global_Market.txt"로 변경
make_changeFilename()
time.sleep (1)
# "HK_Global_Market.txt" 로 변경한 TXT를 읽기 좋게 변경
output_file_name = make_patternFiles()
time.sleep (1)

end_time = datetime.datetime.now()
duration = end_time - start_time
print (f"{datetime.datetime.now()} || Operation Time : {duration}")
time.sleep (2)