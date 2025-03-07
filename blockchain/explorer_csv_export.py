import os
import time
import sys
import os
import csv
import requests
from datetime import datetime


def slow_print(text, delay=0.05, end="\n"):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print(end, flush=True)

def blinking_text(text, repeat=3, delay=0.2):
    for _ in range(repeat):
        sys.stdout.write("\r" + text + " ")
        sys.stdout.flush()
        time.sleep(delay)
        sys.stdout.write("\r" + " " * len(text) + " ")
        sys.stdout.flush()
        time.sleep(delay)
    print("\r" + text)

def scrolling_text(lines, delay=0.05):
    for line in lines:
        slow_print("> " + line + " █", delay=0.03)
        time.sleep(0.2)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def title_screen():
    clear_screen()
    
    # 제목
    title = "█ TOKEN EXPLORER CSV EXPORT █"
    blinking_text(title, repeat=5, delay=0.15)
    
    slow_print("\n[INITIALIZING SYSTEM...]\n", delay=0.1)
    
    messages = [
        "YOU RETRIVED ABOUT TRANSACTION AND TRANSFER INFO FOR TOKEN & COIN",
        "TO PREPARE THAT ADDRESS OF CONTRACT",
        "IF YOU DON`T HAVA ANY ADDRESS, REFER TO SAMPLE HERE",
        "0x3c9764A2644285C88191Af34d1dc9e897b5C0fa9",
        "ACCESS LEVEL: ████ RESTRICTED",
        "SYSTEM STABILITY: NOT TESTED",
        "ACTIVATING SECURE SHELL",
        "CONNECTION ESTABLISHED"
    ]
    
    scrolling_text(messages, delay=0.03)
    
    slow_print("\n>> WELCOME, OUR SYSTEM <<\n", delay=0.1)
    slow_print("🔗 Access Token Explorer → https://explorer.kstadium.io/\n", delay=0.05)

title_screen()

saved_time = datetime.now().strftime("%Y%m%d_%H%M%S")
wei = 1000000000000000000

address = input(f"INPUT THE ADDRESS → ")
tab_selector = input(f"\nWHAT DO YOU WANT MENU?\n1) TRANSACTIONS\n2) TOKEN TRANSFER\n → ")
if tab_selector == "1": # Transactions
    url = f"https://explorer-api.kstadium.io/v1/transaction/list?"
    path_set = f"fromAddress={address}&toAddress={address}&pageNumber=1&pageSize=100&status=1"
    print("select1")
elif tab_selector == "2": # Token Transfer
    url = f"https://explorer-api.kstadium.io/v1/token-transfers"
    path_set = f"/holder-address/{address}?pageNumber=1&pageSize=100"
    print("select2")
else:
    print("ADDRESS IS NOT INVALD IN SYSTEM, PROCESS TOBE CLOSE")
    quit()

def get_explorer_data():
    request_url = f"{url}{path_set}"
    response = requests.get(request_url)
    if response.status_code == 200:
        explorer_result = response.json()
    else:
        print("REQUEST FAILED WITH STATUS CODE: ", response.status_code)
    return explorer_result

def saved_csv_formatted(explorer_result):
    if tab_selector == "1":
        export_dir = os.path.join(os.getcwd(), "export")  # 현재 작업 디렉토리에 'export' 폴더 생성 (없으면 자동 생성)
        os.makedirs(export_dir, exist_ok=True)  # 존재하지 않으면 생성
        csv_file_path = os.path.join(export_dir, f"transaction_data_{address}_{saved_time}.csv")
        header = ["txHash", "method", "blockNumber", "from_address", "to_address", "value", "txFee"]
        with open(csv_file_path, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=header)
            writer.writeheader()
            for tx in explorer_result["data"]["transactionList"]:
                row = {
                    "txHash": tx["txHash"],
                    "method": tx["method"],
                    "blockNumber": tx["blockNumber"],
                    "from_address": tx["from"]["address"],
                    "to_address": tx["to"]["address"],
                    "value": float(tx["value"]) / wei,
                    "txFee": float(tx["txFee"]) / wei
                }
                writer.writerow(row)
        print(f"\nTRANSACTIONS CSV FILE WAS CREATED DONE [{address}]: → {csv_file_path}")
        
    elif tab_selector == "2":
        export_dir = os.path.join(os.getcwd(), "export")
        os.makedirs(export_dir, exist_ok=True) 
        csv_file_path = os.path.join(export_dir, f"token_transfer_data_{address}_{saved_time}.csv")
        header = ["txHash", "method", "blockNumber", "from_address", "to_address", "value", "symbol"]
        with open(csv_file_path, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=header)
            writer.writeheader()
            for tx in explorer_result["data"]["data"]:
                row = {
                    "txHash": tx["transactionHash"],
                    "method": tx["method"],
                    "blockNumber": tx["blockNumber"],
                    "from_address": tx["from"]["address"],
                    "to_address": tx["to"]["address"],
                    "value": float(tx["value"]) / wei,
                    "symbol": tx["symbol"]
                }
                writer.writerow(row)

        print(f"\nTOKEN_TRANSFER_DATA CSV FILE WAS CREATED DONE [{address}]: → {csv_file_path}")
        
    else:
        print(f"THIS {address} IS NOT ANY DATA LOGS. PLEASE CHECK AGAIN")
    
explorer_result = get_explorer_data()
saved_csv_formatted(explorer_result)