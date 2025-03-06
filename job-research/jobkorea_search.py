import os
import csv
import json
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def setup_driver():
    """Chrome WebDriver를 설정하여 반환"""
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # 테스트할 땐 제거 가능
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver

def close_modals(driver):
    """모달 팝업을 감지하고 닫음"""
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    modals = soup.find_all(class_="modal")

    if modals:
        print(f"총 {len(modals)}개의 모달이 발견되었습니다.")
        selenium_modals = driver.find_elements(By.CLASS_NAME, "modal")

        if selenium_modals:
            for modal in selenium_modals:
                try:
                    close_btn = modal.find_element(By.CLASS_NAME, "btnClosePop")
                    close_btn.click()
                    print("모달을 닫았습니다.")
                    time.sleep(1)
                except:
                    print("닫기 버튼을 찾지 못했습니다.")

def search_keyword(driver, word):
    """검색어 입력 후 검색 실행"""
    try:
        smkey_div = driver.find_element(By.CLASS_NAME, "smKey")
        text_input = smkey_div.find_element(By.CSS_SELECTOR, 'input[type="text"]')
        text_input.click()
        text_input.send_keys(word)

        print(f"'{word}' 입력 완료")
        time.sleep(1)

        submit_button = smkey_div.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
        submit_button.click()

        print("검색 버튼 클릭 완료")
    except Exception as e:
        print("오류 발생:", e)

    time.sleep(5)

def extract_list_items(driver):
    """content-list 안의 list-item을 찾아 데이터 추출"""
    items_data = []
    try:
        content_list = driver.find_element(By.CLASS_NAME, "content-list")
        list_items = content_list.find_elements(By.CLASS_NAME, "list-item")

        if list_items:
            print(f"총 {len(list_items)}개의 list-item 발견!")
            for idx, item in enumerate(list_items, start=1):
                data_gavirturl = item.get_attribute("data-gavirturl")
                data_gainfo = item.get_attribute("data-gainfo")

                if data_gavirturl or data_gainfo:
                    item_info = {
                        "index": idx,
                        "data_gavirturl": data_gavirturl,
                        "data_gainfo": data_gainfo
                    }
                    items_data.append(item_info)

                    print(f"{idx}.", end=" ")
                    if data_gavirturl:
                        print(f"data-gavirturl: {data_gavirturl}", end=" ")
                    if data_gainfo:
                        print(f"data-gainfo: {data_gainfo}")
                    print("\n")
        else:
            print("list-item 요소를 찾지 못했습니다.")
    
    except Exception as e:
        print("list-item 추출 중 오류 발생:", e)
    
    return items_data

def save_results(search_word, results):
    """검색 결과를 export 폴더에 txt 및 csv 파일로 저장"""
    export_dir = os.path.join(os.getcwd(), "export")  # 현재 작업 디렉토리에 'export' 폴더 생성 (없으면 자동 생성)
    os.makedirs(export_dir, exist_ok=True)  # 존재하지 않으면 생성

    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    txt_filename = os.path.join(export_dir, f"search_{search_word}_{current_time}.txt")
    csv_filename = os.path.join(export_dir, f"search_{search_word}_{current_time}.csv")

    with open(txt_filename, "w", encoding="utf-8") as txt_file, \
         open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
        
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Index", "채용공고명", "업체명", "직종", "위치", "채용URL", "data-gainfo"])  # CSV 헤더 추가

        for item in results:
            raw_url = item.get("data_gavirturl", "N/A")
            clean_url = raw_url.replace("/virtual", "") if raw_url != "N/A" else "N/A"  # `/virtual` 제거

            data_gainfo_raw = item.get("data_gainfo", "{}")  # JSON 형태의 문자열

            try:
                data_gainfo = json.loads(data_gainfo_raw)  # JSON 변환
            except json.JSONDecodeError:
                data_gainfo = {}  # 오류 발생 시 빈 딕셔너리

            job_title = data_gainfo.get("dimension45", "N/A")  # 채용공고명
            company_name = data_gainfo.get("dimension48", "N/A")  # 업체명
            job_category = data_gainfo.get("dimension66", "N/A")  # 직종
            location = data_gainfo.get("dimension46", "N/A")  # 위치

            # 콘솔 출력
            print(f"{item['index']}. 채용공고명: {job_title}, 업체명: {company_name}, 직종: {job_category}, 위치: {location}, 채용URL: {clean_url}, data-gainfo: {data_gainfo_raw}")

            # TXT 저장
            txt_file.write(f"{item['index']}. 채용공고명: {job_title}, 업체명: {company_name}, 직종: {job_category}, 위치: {location}, 채용URL: {clean_url}, data-gainfo: {data_gainfo_raw}\n")

            # CSV 저장
            csv_writer.writerow([
                item["index"], job_title, company_name, job_category, location, clean_url, data_gainfo_raw
            ])
    
    print(f"결과 저장 완료: {txt_filename}, {csv_filename}")

def process_pages(driver, search_word, total_pages=10):
    """페이지를 순회하며 데이터 추출 및 저장"""
    all_results = []

    for page_no in range(1, total_pages + 1):
        time.sleep(5)  # 페이지 로딩 대기

        print(f"=== Page {page_no} ===")
        page_results = extract_list_items(driver)
        all_results.extend(page_results)

        if page_no < total_pages:
            try:
                next_page_button = driver.find_element(By.CSS_SELECTOR, f'button[data-url*="Page_No={page_no + 1}"]')
                next_page_button.click()
                print(f"Page {page_no + 1}로 이동 중...")
                time.sleep(3)  # 페이지 이동 후 로딩 대기
            except Exception as e:
                print(f"Page {page_no + 1} 버튼을 찾을 수 없음: {e}")
                break  # 버튼을 찾지 못하면 반복 종료

    save_results(search_word, all_results)

# 실행 코드
if __name__ == "__main__":
    driver = setup_driver()
    driver.get("https://www.jobkorea.co.kr/")
    time.sleep(3)

    close_modals(driver)
    
    search_word = "qa"
    search_keyword(driver, search_word)
    
    process_pages(driver, search_word, total_pages=10)

    driver.quit()