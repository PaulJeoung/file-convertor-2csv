from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time
import random
import io
import sys
print (f"{datetime.now()} ||")

# 스크립트 사전 설정 (슬랙, 아이디, 비번, 댓글, 크롬드라이브)
slack_token = ""
channel = ""

login_id = ""
login_pw = ""

tistory_url = 'https://www.tistory.com/'
tistory_feed_url = 'https://www.tistory.com/feed'

comment_text = [
    "포스팅 잘 보았습니다 공감 꾹 누르고 갈께요 (๑˘ꇴ˘๑) \n좋은 하루 보내세요~",
    "좋은 정보 감사합니다   ദി˶ˊᵕˋ˵)  \n잘 보고 머물다 가요~ '◡'✿",
    "구독해 놓고 자주 방문 하고 있답니다\n기분 좋은 하루 보내세요~ (･ω･)b",
    "포스팅 잘 보고 갑니다    ٩(•̤̀ᵕ•̤́๑)૭✧\n공감 꾸우욱~ (b~_^)b",
    "오늘 하루도 힘내시고 뭐든지 득템 하시길 기원 할께요 ४'ٮ'४ \n공감도 꾹 누르고 갑니다",
    "ദ്ദി '֊' ) 우왓!! 너무 좋은 글 잘읽고 갑니다\n공감도 눌렀어요 ദ്ദി⑉¯ ꇴ ¯⑉ )",
    "오늘도 구독자님 블로그 놀러왔어요~ ₍₍ ◝( ◉ ‸ ◉ )◟ ⁾⁾ \n재밌는 글 잘 읽고 공감도 누르고 가요 (●'ᴗ'●)ﾉ♥",
    "뀨~~ ᑦ(・ ﻌ ・)ᐣ 구독자님 새로운글 보러 왔답니다~  \n오늘도 재밌는 하루 보내시길 기도 할께요 ლ(●ↀωↀ●)ლ"
]  # 참고 이모티콘 https://snskeyboard.com/emoticon/

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(tistory_url)
driver.implicitly_wait(2)

def post_tistoryLogin(): # 티스토리 로그인 함수
    print (f"{datetime.now()} || LOGIN_STEP1) MOVE TO TISTORY LOGIN PAGE")
    driver.find_element(By.XPATH, '//*[@id="kakaoHead"]/div/div[3]/div/a').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="cMain"]/div/div/div/a[2]').click()
    time.sleep(1)

    print (f"{datetime.now()} || LOGIN_STEP2) TRY TO TISTORY LOGIN")
    username=driver.find_element(By.XPATH, '//*[@id="loginId--1"]')
    username.send_keys(login_id)
    password=driver.find_element(By.XPATH, '//*[@id="password--2"]')
    password.send_keys(login_pw)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div/form/div[4]/button[1]').click()
    time.sleep(3)

def get_feedList(): # 티스토리 피드에서 피드리스트를 가지고 오는 함수
    print (f"{datetime.now()} || GET_FEEDLIST_STEP1) MOVE TO TISTORY FEED LIST")
    driver.get(tistory_feed_url)
    time.sleep(3)
    
    try:
        driver.execute_script("window.scrollBy(0, 10000);") # 화면을 아래로 스크롤링
        time.sleep(3)
        more_btn = driver.find_element(By.CSS_SELECTOR,"#mArticle > div.section_list.section_list_type2 > button")
        ActionChains(driver).move_to_element(more_btn).perform()
        time.sleep(2)
        print (f"{datetime.now()} || GET_FEEDLIST_STEP2) GET A FEED LISTING AFTER SCROLLING (LESS THEN 90)")
        more_btn.click()
        driver.implicitly_wait(2)
        time.sleep(5)
    except Exception as e:
        print (f"{datetime.now()} || GET_FEEDLIST_STEP2) SCROLLING WAS NOT OPERATION")
   
    print (f"{datetime.now()} || GET_FEEDLIST_STEP3) PRINTING FEED LIST NOW\n")
    html = driver.find_element(By.CLASS_NAME, "list_tistory").get_attribute("innerHTML")
    soup = BeautifulSoup(html.encode("utf-8"),'html.parser')
    urls = {}
    urls=soup.find_all(class_="inner_desc_tit") # 내가 읽을 feed 의 URL 주소만 뽑아오기

    # 가지고 온 URL 을 출력창에 노출 (아래는 for 문 주석 처리 하면 노출 안됨)
    elements = urls
    count = 1
    for element in elements:
        feed_href = element.get('href')
        feed_text = element.get_text(strip=True)
        print(f"[{count}] OF TISTORY TITLE: {feed_text}")
        print(f"[{count}] OF TISTORY URL: {feed_href}")
        count += 1
    print (f"\n{datetime.now()} || GET_FEEDLIST_STEP4) PRINTING FINISHED (Total: {count})\n")
    
    return urls

def get_checkCommnetProperties(feed_href): # 티스토리 블로그에서 닉네임 아이콘 여부로 댓글창을 분류하는 함수
    driver.get(feed_href)
    get_html = driver.page_source
    soup = BeautifulSoup(get_html,'html.parser')
    
    # 닉네임 아이콘이 없는 티스토리 FIND CLASS
    find_div_reply_write = soup.find('div', class_='reply_write') # https://haanss.tistory.com/360
    find_div_comment_form = soup.find('div', class_='comment-form') # https://lswahj.tistory.com/254
    find_div_area_write = soup.find('div', class_ ='area-write') # https://raykim81.tistory.com/261
    find_div_box_comment_write = soup.find('div', class_ ='box_comment_write') # https://fukkifootball.tistory.com/6287
    find_div_commentWrite = soup.find('div', class_ ='commentWrite') # https://leeesann.tistory.com/6297
    
    # 닉네임 아이콘이 있는 티스토리 FIND CLASS
    find_div_tt_wrap_write = soup.find('div', class_='tt_wrap_write') # https://healthbook22.tistory.com/62
    
    if find_div_reply_write: # get_nonameCommnet_a
        # print("TYPE=noname, find_div_reply_write",find_div_reply_write)
        desired_div = find_div_reply_write
        return desired_div
    elif find_div_comment_form:
        # print("TYPE=noname, find_div_comment_form",find_div_comment_form)
        desired_div = find_div_comment_form
        return desired_div
    elif find_div_area_write:
        # print("TYPE=noname, find_div_area_write",find_div_area_write)
        desired_div = find_div_area_write
        return desired_div
    elif find_div_box_comment_write:
        # print("TYPE=noname, find_div_box_comment_write",box_comment_write)
        desired_div = find_div_box_comment_write
        return desired_div
    elif find_div_commentWrite:
        # print("TYPE=noname, find_div_commentWrite",commentWrite)
        desired_div = find_div_commentWrite
        return desired_div
    elif find_div_tt_wrap_write:
        # print("TYPE=name, find_div_tt_wrap_write",find_div_tt_wrap_write)
        desired_div = find_div_tt_wrap_write
        return desired_div
    time.sleep(1)

def get_nonameComment_a(): # 닉네임 아이콘이 없고 CLASS_NAME = reply_write 에서 댓글 남기는 함수
    comment_box = driver.find_element(By.ID, 'comment')
    random_comment = random.choice(comment_text)
    comment_box.send_keys(random_comment)
    time.sleep(1)
    submit_btn = driver.find_element(By.CLASS_NAME, 'btn_register')
    submit_btn.click()
    time.sleep(1)

def get_nonameComment_b(): # 닉네임 아이콘이 없고 CLASS_NAME = comment-form 에서 댓글 남기는 함수
    try:
        comment_box = driver.find_element(By.ID, 'comment')
        random_comment = random.choice(comment_text)
        comment_box.send_keys(random_comment)
        time.sleep(1)
        submit_btn = driver.find_element(By.CLASS_NAME, 'btn')
        submit_btn.click()
        time.sleep(1)
    except NoSuchElementException:
        try:
            comment_box = driver.find_element(By.CSS_SELECTOR, 'textarea[name="comment"]')
            random_comment = random.choice(comment_text)
            comment_box.send_keys(random_comment)
            time.sleep(1)
            submit_btn = driver.find_element(By.CLASS_NAME, 'btn')
            # submit_btn.click()
            time.sleep(1)
        except NoSuchElementException:
            print("{datetime.now()} || LIKE & COMMENT_STEP4) WARNING!! NONAME_TYPE_B FAILED")
        
def get_nonameComment_c(): # 닉네임 아이콘이 없고 CLASS_NAME = area-write 에서 댓글 남기는 함수
    comment_box = driver.find_element(By.ID, 'comment')
    random_comment = random.choice(comment_text)
    comment_box.send_keys(random_comment)
    time.sleep(1)
    submit_btn = driver.find_element(By.CLASS_NAME, 'btn_register')
    submit_btn.click()
    time.sleep(1)

def get_nonameComment_d(): # 닉네임 아이콘이 없고 CLASS_NAME = box_comment_write 에서 댓글 남기는 함수
    comment_box = driver.find_element(By.ID, 'comment')
    random_comment = random.choice(comment_text)
    comment_box.send_keys(random_comment)
    time.sleep(1)
    submit_btn = driver.find_element(By.CLASS_NAME, 'btn_register')
    submit_btn.click()
    time.sleep(1)
    
def get_nonameComment_e(): # 닉네임 아이콘이 없고 CLASS_NAME = commentWrite 에서 댓글 남기는 함수
    comment_box = driver.find_element(By.CSS_SELECTOR, 'textarea[name="comment"]')
    random_comment = random.choice(comment_text)
    comment_box.send_keys(random_comment)
    time.sleep(1)
    submit_btn = driver.find_element(By.CLASS_NAME, 'submit')
    submit_btn.click()
    time.sleep(1)

def get_nameComment_a(): # 닉네임 아이콘이 있고 CLASS_NAME = tt_wrap_write 에서 댓글 남기는 함수
    comment_box = driver.find_element(By.CLASS_NAME, 'tt-cmt')
    random_comment = random.choice(comment_text)
    comment_box.send_keys(random_comment)
    time.sleep(1)
    submit_btn = driver.find_element(By.CLASS_NAME, 'tt-btn_register')
    submit_btn.click()
    time.sleep(1)

def post_feedCommnet(urls): # 구독한 피드리스트에 접속 후 공감 댓글 작성 하는 함수
    count = 1
    for url in urls:
        #### 공감 프로세스 ####
        time.sleep(2) # 새로운 페이지 이동 후 로딩 대기 -> 미사용 driver.implicitly_wait(2)
        try:
            feed_href = url.get('href')
            print (f"\n{datetime.now()} || LIKE & COMMENT_STEP1) [{count}] TISTORY PAGE MOVE >>> ({feed_href})")
            desired_div_html = get_checkCommnetProperties(feed_href)
            driver.get(feed_href) # feed_href
            time.sleep(2)
            driver.execute_script("window.scrollBy(0, 2000);")
            time.sleep(1)
            like_btn = driver.find_element(By.CLASS_NAME, "wrap_btn")
            ActionChains(driver).move_to_element(like_btn).perform()
            like_btn.click()
            time.sleep(1)
            print (f"{datetime.now()} || LIKE & COMMENT_STEP2) CLICK THE LIKE BUTTON")
        except:
            print (f"{datetime.now()} || LIKE & COMMENT_STEP2) LIKE BUTTON CANNOT FINDED T_T")
        #### 댓글 프로세스 ####
        try:
            desired_div = f"{desired_div_html}"
            print(f"{datetime.now()} || LIKE & COMMENT_STEP3) MOVE FOR COMMENT WRRITING")
            if "reply_write" in desired_div:
                get_nonameComment_a()
                print(f"{datetime.now()} || LIKE & COMMENT_STEP4) NONAME_TYPE_A WRRITING SUCCESSED")
            elif "comment-form" in desired_div:
                get_nonameComment_b()
                print(f"{datetime.now()} || LIKE & COMMENT_STEP4) NONAME_TYPE_B WRRITING SUCCESSED")
            elif "area-write" in desired_div:
                get_nonameComment_c()
                print(f"{datetime.now()} || LIKE & COMMENT_STEP4) NONAME_TYPE_C WRRITING SUCCESSED")
            elif "box_comment_write" in desired_div:
                get_nonameComment_d()
                print(f"{datetime.now()} || LIKE & COMMENT_STEP4) NONAME_TYPE_D WRRITING SUCCESSED")
            elif "commentWrite" in desired_div:
                get_nonameComment_e()
                print(f"{datetime.now()} || LIKE & COMMENT_STEP4) NONAME_TYPE_E WRRITING SUCCESSED")
            elif "tt_wrap_write" in desired_div:
                get_nameComment_a()
                print(f"{datetime.now()} || LIKE & COMMENT_STEP4) NICK_NAME_TYPE_A WRRITING SUCCESSED")
            else:
                print(f"{datetime.now()} || LIKE & COMMENT_STEP3) WARNING!! COMMENT BOX NOT FOUND")
        except:
            print(f"{datetime.now()} || LIKE & COMMENT_STEP3) WARNING EXCEPTION !! COMMENT BOX NOT FOUND")
        count += 1

def send_slack_message (slack_message): # 슬랙 paul_tissue 채널에 결과를 전송하는 함수
    requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+slack_token},
        data={
            "channel": channel,"text": slack_message
            })

def warp_theStartStreamIO(): # output stream으 로 묶는 함수
    output_stream = io.StringIO()
    sys.stdout = output_stream
    return output_stream
    
def warp_theEndStreamIO(output_stream): # output stream 을 종료하는 함수
    sys.stdout = sys.__stdout__
    output_string = output_stream.getvalue()
    slack_message = f"```{output_string}```"
    return slack_message

log_msg = warp_theStartStreamIO()
start_time = datetime.now()
print (f"{datetime.now()} || {login_id}`S TISTORY LIKE & COMMENT SCRIPT START :", start_time)
slack_message = warp_theEndStreamIO(log_msg)
send_slack = send_slack_message (slack_message)

post_tistoryLogin()
urls = get_feedList()
post_feedCommnet(urls)

# output stream 적용 시작
log_msg = warp_theStartStreamIO()
end_time = datetime.now()
print (f"{datetime.now()} || {login_id}`S TISTORY LIKE & COMMENT SCRIPT FINISH : {end_time}, TOTAL DURATION : {end_time - start_time}")

# 셀레니움 종료
time.sleep(2)
driver.quit()

# output stream 에 적용된 print 내용을 슬랙으로 전송
slack_message = warp_theEndStreamIO(log_msg)
send_slack = send_slack_message (slack_message)