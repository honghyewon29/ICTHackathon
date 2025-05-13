import requests
from bs4 import BeautifulSoup
import datetime
import os
import schedule
import time

CURRENT_FILE = "LLM\current_bbsno.txt"
OUTPUT_FILE = "LLM\Data\통합공지.txt"

BASE_URL = "https://www.suwon.ac.kr/index.html"
PARAMS = {
    "menuno": "674",
    "boardno": "667",
    "siteno": "37",
    "act": "view"
}
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_current_bbsno():
    if not os.path.exists(CURRENT_FILE):
        with open(CURRENT_FILE, "w") as f:
            f.write("87460")
    with open(CURRENT_FILE, "r") as f:
        return int(f.read().strip())

def save_current_bbsno(bbsno):
    with open(CURRENT_FILE, "w") as f:
        f.write(str(bbsno))

def fetch_new_notices():
    current_bbsno = get_current_bbsno()
    today_str = datetime.datetime.now().strftime("%Y%m%d")
    new_file_created = False

    while True:
        next_bbsno = current_bbsno + 1
        PARAMS["bbsno"] = str(next_bbsno)
        res = requests.get(BASE_URL, params=PARAMS, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")

        title_tag = soup.select_one("div.board_viewtitle > h3")
        body_tag = soup.select_one("div.board_viewcont")

        if title_tag and body_tag:
            title = title_tag.get_text(strip=True)
            body = body_tag.get_text(strip=True)
            link = f"https://www.suwon.ac.kr/index.html?menuno=674&boardno=667&siteno=37&act=view&bbsno={next_bbsno}"

            with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                f.write(f"[제목]: {title}\n[링크]: {link}\n[본문]: {body}\n\n")
                print(f"{next_bbsno}번 저장 완료")

            current_bbsno = next_bbsno
            save_current_bbsno(current_bbsno)

        else:
            print(f"{next_bbsno}번은 아직 없음. 대기.")
            break

schedule.every().day.at("00:00").do(fetch_new_notices)

print("스케줄러 실행 중... 매일 00시에 새 공지 확인.")

fetch_new_notices() # 초기 실행

while True:
    schedule.run_pending()
    time.sleep(1)