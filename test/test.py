import requests
from bs4 import BeautifulSoup
import time
import random
import sqlite3
from datetime import datetime

from aiogram import F, Router
from aiogram.types import CallbackQuery

now = datetime.now()
day_today = now.strftime("%d.%m")
current_time = now.strftime("%H-%M")

with sqlite3.connect("db/calendar.db") as con:
    cur = con.cursor()
    # Ищем записи с сегодняшней датой и временем, не превышающим текущее
    cur.execute(
        "SELECT date, time, event FROM onetime_reminders WHERE date = ? AND time <= ?",
        (day_today, current_time),
    )
    # На выходе получаем список кортежей(дата, событие)
    result = cur.fetchall()

    if result:
        text = f"Сегодня {day_today}:\n"

        for _, time_event, event in result:
            text += f"{time_event.ljust(5)} - {event}\n"

        print(text)
