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

date_elements = soup.find_all(class_="tournament-calendar__date")
event_elements = soup.find_all(class_="tournament-calendar__name")

with sq.connect("db/calendar.db") as con:
    cur = con.cursor()

    # Сначала создаем таблицу (если её нет)
    cur.execute(
        """CREATE TABLE IF NOT EXISTS f1_calendar (
                date TEXT,
                event TEXT
                )"""
    )

    # Потом очищаем её (теперь таблица точно существует)
    cur.execute("DELETE FROM f1_calendar")

    for date_elem, event_elem in zip(date_elements, event_elements):
        event_text = event_elem.text.strip()

        if "гонка" in event_text.lower() or (
            "спринт" in event_text.lower() and "квалификация" not in event_text.lower()
        ):
            date_text = date_elem.text.strip()

            try:
                # Пробуем распарсить с временем
                dt = datetime.strptime(date_text, "%d.%m.%Y %H:%M")
            except ValueError:
                # Если не получается, пробуем только дату
                dt = datetime.strptime(date_text, "%d.%m.%Y")

            # Добавляем 2 часа
            dt = dt + timedelta(hours=2)

            cur.execute(
                "INSERT INTO f1_calendar (date, event) VALUES (?, ?)",
                (dt.strftime("%Y-%m-%d %H:%M"), event_text),
            )
