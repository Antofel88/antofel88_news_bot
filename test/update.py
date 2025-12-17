import requests
from bs4 import BeautifulSoup
import sqlite3 as sq
from datetime import datetime, timedelta


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}


url = "https://www.sports.ru/hockey/club/edmonton-oilers/calendar/"
response = requests.get(url=url, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

date = soup.find("tbody").find_all(class_="name-td alLeft bordR")
team = soup.find("tbody").find_all(class_="name-td alLeft")
score = soup.find("tbody").find_all(class_="score")
home_guest = soup.find("tbody").find_all(class_="alRight padR20")

date = [i for i in date if "|" in i.text]
team = [
    i
    for i in team
    if ("НХЛ" not in i.text.upper()) and ("КУБОК СТЭНЛИ" not in i.text.upper())
]

with sq.connect("db/calendar.db") as con:
    cur = con.cursor()

    cur.execute(f"""DELETE FROM edmonton_calendar""")

    cur.execute(
        """CREATE TABLE IF NOT EXISTS edmonton_calendar (
                date TEXT,
                team TEXT,
                home_guest TEXT,
                score TEXT
                )"""
    )

    for item in zip(date, team, home_guest, score):
        cur.execute(
            f"""INSERT INTO edmonton_calendar (date, team, home_guest, score) VALUES ("{ (
            datetime.strptime(item[0].text.strip(), "%d.%m.%Y|%H:%M")
            + timedelta(hours=2)
        ).strftime("%Y-%m-%d %H:%M")}", "{item[1].text.strip()}", "{item[2].text.strip().lower()}", "{item[3].text.strip().replace("\n", " ")}")"""
        )


# with sq.connect("db/calendar.db") as con:
#     cur = con.cursor()

#     cur.execute(
#         """CREATE TABLE IF NOT EXISTS edmonton_calendar (
#                 date TEXT,
#                 team TEXT,
#                 home_guest TEXT,
#                 score TEXT
#                 )"""
#     )
