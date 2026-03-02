import requests
from bs4 import BeautifulSoup
import sqlite3 as sq
from datetime import datetime, timedelta

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}


url = "https://www.championat.com/auto/_f1/tournament/1032/calendar/"
response = requests.get(url=url, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

date = soup.find_all(class_="tournament-calendar__date")
event = soup.find_all(class_="tournament-calendar__name")


with sq.connect("db/calendar.db") as con:
    cur = con.cursor()

    cur.execute(f"""DELETE FROM f1_calendar""")

    cur.execute(
        """CREATE TABLE IF NOT EXISTS f1_calendar (
                date TEXT,
                event TEXT
                )"""
    )

    for item in zip(date, event):
        if "гонка" in item[1].text.lower() or (
            "спринт" in item[1].text.lower()
            and "квалификация" not in item[1].text.lower()
        ):
            cur.execute(
                f"""INSERT INTO f1_calendar (date, event) VALUES ("{(
                datetime.strptime(item[0].text.strip(), "%d.%m.%Y %H:%M")
                + timedelta(hours=2)
            ).strftime("%Y-%m-%d %H:%M")}", "{item[1].text.strip()}")"""
            )
