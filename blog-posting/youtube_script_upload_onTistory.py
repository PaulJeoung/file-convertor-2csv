import requests
import time
import datetime
import io
import random
import os
import sys
print (f"{datetime.datetime.now()} || UPLOAD SCRIPT START")
# ---------- 정보세트 ----------  # API 등록은 https://www.tistory.com/guide/api/manage/register 에서...
slack_token = ""
channel = ""

login_id = ""
login_pw = ""
app_id = ""
app_secretKey = ""
app_service_url = "https://{tistory_name}.tistory.com/"
category_id = "1132625"
oauth_token = ""

today = datetime.date.today()
formatted_date = today.strftime("%m/%d")
post_contents = f"/Users/pj/Downloads/HK_Global_Market_{today}.txt"
tistory_url = "https://www.tistory.com/"

# 1회성 사용
def get_tistoryAuth():
    # 1번만 필요 합니다요
    # auth_code_url = f"https://www.tistory.com/oauth/authorize?client_id={app_id}&redirect_uri={app_service_url}&response_type=code"
    # print (auth_code_url)
    
    # auth_code에 코드 들어 갔으면 위에는 주석
    auth_code = ""
    
    oauth_token_url = f"https://www.tistory.com/oauth/access_token?client_id={app_id}&client_secret={app_secretKey}&redirect_uri={app_service_url}&code={auth_code}&grant_type=authorization_code"
    print (f"{datetime.datetime.now()} || {oauth_token_url}")
    oauth_token = ""
    return oauth_token

def random_image(): # 업로드 할 이미지 랜덤으로 설정
    folder_path = '/Users/{folder_name}/Downloads/hk_global/img'
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        files = os.listdir(folder_path)
        files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
        if len(files) >= 9:
            selected_file = random.choice(files)
            print(f"{datetime.datetime.now()} || SELECTED IMAGE FILES: {selected_file}")
            return selected_file
        else:
            print(f"{datetime.datetime.now()} || LESS THEN 9 IMAGE FILES IN FOLDER, ADD TO MORE IMAGE")
    else:
        print(f"{datetime.datetime.now()} ||DIRECTORY IS NOT EXIST")

def image_upload(): # 이미지 업로드 후 주소 가져오기
    attched_url = 'https://www.tistory.com/apis/post/attach'
    folder_path = f"/Users/{folder_name}/Downloads/hk_global/img/{selected_file}"
    files = {'uploadedfile' : open(folder_path,'rb')}
    params = {
        'access_token': oauth_token,
        'blogName': tistory_name,
        'targetUrl' : tistory_name,
        'output' : 'json'
    }
    # print(f"{params}")
    response = requests.post(attched_url, params=params, files=files)
    if response.status_code == 200:
        data = response.json()
        image_url = data['tistory']['url']
        replacer_url = data['tistory']['replacer']
        print (f"{datetime.datetime.now()} || UPLOAD IMAGE API POST REQUESTS SUCCESSED\n{data}")
    else:
        print (f"{datetime.datetime.now()} || IMAGE API UPLOADED FAIL... \n{response.status_code}")
    return image_url, replacer_url
        
def formatted_textToHtml():
    with open(post_contents, 'r+', encoding='utf-8') as file:
        first_line = file.readline().strip()

    if "헤드라인" in first_line:
        index = first_line.index("헤드라인")
        headline_title = first_line[:index].strip()

    with open(post_contents, 'r+', encoding='utf-8') as file:
        text = file.read()
        file.seek(0, 2)
        file.write(f"\n\n{image_url}")
        
    with open(post_contents, 'r', encoding='utf-8') as file:
        text_content = file.read()

    return headline_title, text_content

def tistory_write():
    post_endpoint = 'https://www.tistory.com/apis/post/write'

    # 요청 매개변수 설정
    output_type = 'json'
    blog_name = tistory_name  # {tistory_name}.tistory.com 주소 중 앞에 이름
    title = headline_title # f"{formatted_date} 글로벌 마켓" # 제목
    content = text_content # 내용
    visibility = 2 # 0: 비공개, 1: 보호, 2: 발행
    categoryId = category_id  # 카테고리 ID -> tstory_category 함수에서 확인 가능
    published = 'false'  # 공개 예약 여부
    slogan = '' # 글 슬로건
    tag = '당잠사, 한경글로벌, 해외시황, 미국증시, 카카오떡락 되서 내주식망함' # 태그 (선택 사항)
    accept_comment = 1  # 댓글 허용 여부
    password = ''  # 글 비밀번호 (선택 사항)
    
    data = { # 대용량 글을 업로드 할때 414 에러가 발생해 params 대신 data 로 전송
        'access_token': oauth_token,
        'output': output_type,
        'blogName': blog_name,
        'title': title, 
        'content': content,
        'visibility': visibility,
        'category': categoryId,
        'published': published,
        'slogan': slogan,
        'tag': tag,
        'acceptComment': accept_comment,
        'password': password
    }
    print (f"{datetime.datetime.now()} || POST API SENDS NOW AT TISTORY")
    response = requests.post(post_endpoint, data=data) # params=params
    if response.status_code == 200:
        data = response.json()
        print (f"{datetime.datetime.now()} || API POST REQUESTS SUCCESSED\n{data}")
    else:
        print (f"{datetime.datetime.now()} || POST API UPLOADED FAIL... \n{response.status_code}")
    return data

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
start_time = datetime.datetime.now()
print (f"{start_time} || 떡상떡락`S DANGJAMSA POSTING '{post_contents}'")
slack_message = warp_theEndStreamIO(log_msg)
send_slack = send_slack_message (slack_message)

##### 당잠사 실행 #####
selected_file = random_image()
image_url, replacer_url = image_upload()
headline_title, text_content = formatted_textToHtml()
result = tistory_write()
print (f"{datetime.datetime.now()} || TODAY`S DANGJAMSA UPLOADED WAS DONE")
##### 당잠사 실행 #####

log_msg = warp_theStartStreamIO()
print(f"SELECTED TODAY IMAGES : {selected_file}\nTHUMBNAIL IMAGE LINK : {image_url}\nPOSTING TITLE : {headline_title}\nPOST API RESPONSE : {result}")
end_time = datetime.datetime.now()
print (f"{end_time} || Total Operation Time : {end_time - start_time}")
time.sleep(2)
slack_message = warp_theEndStreamIO(log_msg)
send_slack = send_slack_message (slack_message)