import requests
from bs4 import BeautifulSoup
import schedule
import time
import os

OUTPUT_FILE = "LLM\Data\식단표.txt"

def fetch_meal_info(menuno, place_name, wanted_meals):
    url = f"https://www.suwon.ac.kr/index.html?menuno={menuno}"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")

    table = None
    for t in soup.select("table"):
        caption = t.find("caption")
        if caption and "학생 식단표" in caption.get_text():
            table = t
            break

    if not table:
        result = f"[{place_name}] 식단표를 찾을 수 없습니다.\n"
        return result

    weekdays = ["월", "화", "수", "목", "금"]
    rows = table.select("tbody > tr")
    result = ""

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 7:
            continue

        meal_type = cells[0].get_text(strip=True)
        if meal_type not in wanted_meals:
            continue

        price_info = cells[1].get_text(strip=True)
        menus = []
        for day, cell in zip(weekdays, cells[2:]):
            items = [line.strip() for line in cell.stripped_strings]
            menu = " ".join(items)
            menus.append(f"[{day}요일]\n{menu}")

        result += f"\n===== {place_name} ({meal_type}) =====\n"
        result += f"가격/분류: {price_info}\n"
        result += "\n".join(menus)
        result += "\n" + "=" * 40 + "\n"

    if result == "":
        result = f"[{place_name}] 해당 식단 없음.\n"

    return result

def fetch_new_notices():

    os.makedirs("Data", exist_ok=True)

    data1 = fetch_meal_info(1792, "종합강의동 식당", ["중식", "중식"])  
    data2 = fetch_meal_info(1793, "아마랜스홀 식당", ["중식", "석식"])

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        if data1:
            f.write(data1)
        if data2:
            f.write(data2)

    print("Data/식단표.txt 저장 완료!")

schedule.every().sunday.at("00:00").do(fetch_new_notices)

print("스케줄러 실행 중...")


fetch_new_notices()

while True:
    schedule.run_pending()
    time.sleep(1)
