from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
import requests
import json
import time
import sys

# xrp ledger testnet faucet : https://xrpl.org/resources/dev-tools/tx-sender
# xrp ledger testnet explorer : https://testnet.xrpl.org/

destination_account = input(f"{datetime.now()} || 테스트넷에서 XPR를 받을 주소를 넣어 주세요 → ")
# destination_account = "{계속 사용하는 계정은 위의 주석을 제거하고 여기에 계정을 넣어주세요}"

print ("\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
print (f"\n{datetime.now()} || XRP Faucet에서 XRP를 전송 하겠습니다")

xrp_testnet_faucet= "https://xrpl.org/tx-sender.html"
xrp_testnet_explorer = "https://testnet.xrpl.org/accounts/"
network_url = "https://s.altnet.rippletest.net:51234/" # Testnet
# network_url = "https://xrplcluster.com/" # Mainnet

# 크롬드라이버 사용
chrome_options = Options()
chrome_options.add_argument("--window-size=1600,1200")
driver = webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()))

def exec_Loadingbar(contents, duration, steps=1): # faucet 시간 동안 사용할 프로그레시브바
    for _ in range(duration):
        sys.stdout.write("\r" + "■" * _ + " " * (steps - _) + f" {(_ / duration) * 100:.2f}%")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write(f"\n{contents} COMPLETE !!\n")

def get_xrpBalanceInfo(): # 사용자 지갑의 잔액 조회
    headers = {'Content-Type': 'application/json'}
    data = {
        "method": "account_info",
        "params": [
            {"account": destination_account, "ledger_index": "current", "queue": True}
        ]
    }
    response = requests.post(network_url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        result = response.json()
        balance = float(result['result']['account_data']['Balance']) / 1000000
        txhash = result['result']['account_data']['PreviousTxnID']
        print (f"\n{datetime.now()} || {destination_account} XRP Wallet Balance : {balance}")
        print (f"{datetime.now()} || Recently txhash : {txhash}\n")
    else:
        print(f"\n{datetime.now()} || Error: {response.status_code}, {response.text}\n")

def exec_transferXRP():
    # 1. Destination Address 입력
    input_dest_box = driver.find_element(By.ID, 'destination_address')
    input_dest_box.clear()
    time.sleep(2)
    input_dest_box.send_keys(destination_account)
    print(f"{datetime.now()} || XRP를 전송할 주소는 {destination_account} 입니다")
    time.sleep(2)

    # 2. Initialize 수행
    init_btn = driver.find_element(By.ID, 'init_button')
    init_btn.click()
    print(f"{datetime.now()} || Initialize를 시작 하겠습니다. 이 작업은 10~30초 정도 소요됩니다")
    time.sleep(2)
    
    # 3. Send amount 입력
    amount = 9980000000
    input_amount_box = driver.find_element(By.ID, 'send_xrp_payment_amount')
    input_amount_box.clear()
    time.sleep(1)
    input_amount_box.send_keys(amount)
    loading_time = 30
    exec_Loadingbar("Initializing", loading_time)
    print(f"{datetime.now()} || Initialize가 완료 되었습니다")
    print(f"{datetime.now()} || XRP faucet에서 {amount/1000000} XRP를 전송하겠습니다")
    
    # 4. Send XRP
    print(f"{datetime.now()} || XRP 전송 중입니다. 이 작업은 10초 정도 소요 됩니다")
    send_xrp_btn = driver.find_element(By.ID, 'send_xrp_payment_btn')
    send_xrp_btn.click()
    loading_time = 10
    exec_Loadingbar("Transferring", loading_time)
    
# while True:
for _ in range(30):
    get_xrpBalanceInfo()
    driver.get(xrp_testnet_faucet)
    exec_transferXRP()
    get_xrpBalanceInfo()
    print(f"{datetime.now()} || 자세한 내용은 Testnet XRP에서 확인하세요 {xrp_testnet_explorer}{destination_account}\n")
    time.sleep (5)
