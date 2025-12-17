import requests
from bs4 import BeautifulSoup
import time
import random
import sqlite3
from datetime import datetime

from aiogram import F, Router
from aiogram.types import CallbackQuery

day_today = datetime.now().strftime("%d")

with sqlite3.connect("db/calendar.db") as con:
    cur = con.cursor()
    cur.execute(
        "SELECT date, event FROM monthly_reminders WHERE date LIKE ?",
        (f"{day_today}%",),
    )
    result = cur.fetchall()

if result:
    text = f"Сегодня {day_today} число:\n"

    for _, event in result:
        text += f"{event}\n"


print(text)
