import requests
from bs4 import BeautifulSoup
import os
import schedule
import time

OUTPUT_FILE = "LLM/Data/식단표.txt"
os.makedirs("LLM/Data", exist_ok=True)

def clean_text(html):
    return html.get_text(separator=' ', strip=True).replace('\xa0', ' ').replace('  ', ' ')

def parse_single_row_tds(tds, title):
    """td 배열만 받아서 월~금까지 파싱"""
    days = ["월요일", "화요일", "수요일", "목요일", "금요일"]
    result = f"===== {title} =====\n"
    for i, day in enumerate(days):
        result += f"[{day}]\n{clean_text(tds[i])}\n"
    result += "========================================\n\n"
    return result

def fetch_meals():
    result = ""

    url_1792 = "https://www.suwon.ac.kr/index.html?menuno=1792"
    res1 = requests.get(url_1792, headers={"User-Agent": "Mozilla/5.0"})
    soup1 = BeautifulSoup(res1.text, "html.parser")

    table1 = soup1.select_one("div#contents_table2 table")
    if table1:
        tds1 = table1.select("tbody > tr")[0].select("td")[2:]  # 앞에 2개는 구분/코너명
        result += parse_single_row_tds(tds1, "종합강의동 학생 식당 (중식)")

    table2 = soup1.select_one("div#teMn table")
    if table2:
        tds2 = table2.select("tbody > tr")[0].select("td")[1:]  # 첫 td는 구분
        result += parse_single_row_tds(tds2, "종합강의동 교직원원 식당 (중식)")

    url_1793 = "https://www.suwon.ac.kr/index.html?menuno=1793"
    res2 = requests.get(url_1793, headers={"User-Agent": "Mozilla/5.0"})
    soup2 = BeautifulSoup(res2.text, "html.parser")
    table3 = soup2.select_one("div#contents_table22 table")

    if table3:
        rows = table3.select("tbody > tr")
        if len(rows) >= 2:
            tds3_lunch = rows[0].select("td")[2:]  
            result += parse_single_row_tds(tds3_lunch, "아마랜스홀 식당 (중식)")

            tds3_dinner = rows[1].select("td")[2:]  
            result += parse_single_row_tds(tds3_dinner, "아마랜스홀 식당 (석식)")

    return result

def save_to_file():
    menu_text = fetch_meals()
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(menu_text)
    print(f"✅ 식단표 저장 완료: {OUTPUT_FILE}")

import requests
from bs4 import BeautifulSoup
import os

OUTPUT_FILE = "LLM/Data/식단표.txt"
os.makedirs("LLM/Data", exist_ok=True)

def clean_text(html):
    return html.get_text(separator=' ', strip=True).replace('\xa0', ' ').replace('  ', ' ')

def parse_single_row_tds(tds, title):
    """td 배열만 받아서 월~금까지 파싱"""
    days = ["월요일", "화요일", "수요일", "목요일", "금요일"]
    result = f"===== {title} =====\n"
    for i, day in enumerate(days):
        result += f"[{day}]\n{clean_text(tds[i])}\n"
    result += "========================================\n\n"
    return result

def fetch_meals():
    result = ""

    url_1792 = "https://www.suwon.ac.kr/index.html?menuno=1792"
    res1 = requests.get(url_1792, headers={"User-Agent": "Mozilla/5.0"})
    soup1 = BeautifulSoup(res1.text, "html.parser")

    table1 = soup1.select_one("div#contents_table2 table")
    if table1:
        tds1 = table1.select("tbody > tr")[0].select("td")[2:]  # 앞에 2개는 구분/코너명
        result += parse_single_row_tds(tds1, "종합강의동 학생 식당 (중식)")

    table2 = soup1.select_one("div#teMn table")
    if table2:
        tds2 = table2.select("tbody > tr")[0].select("td")[1:]  # 첫 td는 구분
        result += parse_single_row_tds(tds2, "종합강의동 교직원원 식당 (중식)")

    url_1793 = "https://www.suwon.ac.kr/index.html?menuno=1793"
    res2 = requests.get(url_1793, headers={"User-Agent": "Mozilla/5.0"})
    soup2 = BeautifulSoup(res2.text, "html.parser")
    table3 = soup2.select_one("div#contents_table22 table")

    if table3:
        rows = table3.select("tbody > tr")
        if len(rows) >= 2:
            tds3_lunch = rows[0].select("td")[2:]  
            result += parse_single_row_tds(tds3_lunch, "아마랜스홀 식당 (중식)")

            tds3_dinner = rows[1].select("td")[2:]  
            result += parse_single_row_tds(tds3_dinner, "아마랜스홀 식당 (석식)")

    return result

def save_to_file():
    menu_text = fetch_meals()
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(menu_text)
    print(f"✅ 식단표 저장 완료: {OUTPUT_FILE}")

if __name__ == "__main__":
    
    save_to_file()  # 처음 실행 시 바로 저장
    
    schedule.every().sunday.at("00:00").do(save_to_file)  # 월요일 00시에 실행

    print("🕒 매주 일요일 00시에 식단표를 저장합니다.")
    while True:
        schedule.run_pending()
        time.sleep(60)  # 1분마다 체크