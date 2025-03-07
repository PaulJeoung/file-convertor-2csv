** 저장을 위한 공간은 mac, windows 환경을 따로 지정 하지 않았기 때문에 필요할때 수정 해주세요 **

## I. python 사용을 위한 가상 환경 설정

1. python3 -m venv venv
2. source venv/bin/activate
3. 가상환경 종료
    - deactivate

## II. 파일 실행

*.py 실행을 위한 module 설치 (pip)

이후 각 파일들을 실행

1. /job-reasearch
    - 채용사이트 검색어 검색 및 저장
    - pip install selenium webdriver-manager
    - pip install beautifulsoup4

2. /cloudwatch-file-convert
    - cloudwatch에 있는 데이터를 spreadsheet 파일로 변환
    - pip install pandas

3. /blockchain
    - 블록체인 계약 주소로 거래 현황 조회 및 파일 변환
    - pip install requests
    - pip install xrpl-py

4. /gui-boxes
    - gui 용 시스템 제작