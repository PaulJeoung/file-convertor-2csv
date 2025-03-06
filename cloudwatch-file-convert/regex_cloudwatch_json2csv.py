import csv
import json
import pandas as pd
from datetime import datetime

dir_name = "" # 다운로드 폴더 앞에 개인 랩탑 폴더 이름을 적어주세요
saved_time = timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

download_file = f"/Users/{dir_name}/Downloads/logs-insights-results.csv"
change_file = f"/Users/{dir_name}/Downloads/logs-insights-results_{saved_time}.csv"

def extract_fields(message):
    data = json.loads(message)
    timestamp = data.get('timestamp')
    http_method = data.get('http_method')
    user_id = data.get('user_id')
    request_uri = data.get('request_uri')
    response_body = data.get('response_body', {})
    status_code = data.get('status_code')
    txhash = response_body.get('txhash')
    request_body = json.dumps(data.get('request_body', {}))
    
    return timestamp, http_method, user_id, request_uri, status_code, txhash, request_body

with open(download_file, 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    extracted_data = []
    for row in reader:
        message = row['@message']
        fields = extract_fields(message)
        extracted_data.append(fields)
    
headers = ['Timestamp(UTC)', 'HTTP Method', 'User ID', 'Request URI', 'status_code', 'TX Hash', 'Request Body']
with open(f"{change_file}", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    writer.writerows(extracted_data) 

print(f"CSV 파일을 다른이름으로 저장 했습니다 :{change_file}.")