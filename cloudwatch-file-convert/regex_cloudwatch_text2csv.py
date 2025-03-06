import pandas as pd
from datetime import datetime

#####################################################################################
####                      Clouldwatch csv transfer manual                      ######
####                                                                           ######
####                   1. AWS 쿼리 조회 결과 파일을 CSV 로 다운로드                    ######
####              2. 다운로드 받은 파일을 아래 df = pd.read_csv 이하 경로에 추가         ######
####                    3. 저장한 위치를 output_file 이하 경로에 추가                 ######
####                      4. 조회에 필요한 패턴은 잘 추가 해주세요                      ######
####                                                                           ######
####                  **업체명** 관련 조회 쿼리를 기준으로 작성 되었습니다                 ######
#####################################################################################

# 패턴 분류 하려는 csv 파일 위치
# AWS 에서 csv 파일을 다운 받으면, logs-insights-results.csv 저장
# df = pd.read_csv('/Users/{user_name}/Downloads/logs-insights-results.csv')
df = pd.read_csv('/Users/pj/Downloads/logs-insights-results.csv')

# print(df.columns)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

get_uri_pattern = r"\[GET\]\s*\[URI:(.*?)\]"
post_uri_pattern = r"\[POST\]\s*\[URI:(.*?)\]"
user_pattern = r"\[USER:(.*?)\]"
request_body_pattern = r"\[REQUEST BODY:(.*?)\]"
response_error_pattern = r"\[RESPONSE:(.*?)\]"

df['URI'] = df['@message'].str.extract(get_uri_pattern, expand=False)
df['URI'] = df['@message'].str.extract(post_uri_pattern, expand=False)
df['USER ID'] = df['@message'].str.extract(user_pattern, expand=False)
df['REQUEST'] = df['@message'].str.extract(request_body_pattern, expand=False)
df['RESONSE'] = df['@message'].str.extract(response_error_pattern, expand=False)

# 패턴 출력 하는 new csv 파일
user_name = input (f"/Users/ooo/Downloads/ 의 ooo 폴더 네임을 알려주세요")
output_file = f'/Users/{user_name}/Downloads/logs-insights-results_{timestamp}.csv'
df.to_csv(output_file, index=False)

print(f"The new file creates that to making C column. Filename :{output_file}.")