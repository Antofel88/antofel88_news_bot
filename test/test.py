import requests
from bs4 import BeautifulSoup
import time
import random
import sqlite3
from datetime import datetime

from aiogram import F, Router
from aiogram.types import CallbackQuery

# Создаем объект текущей даты, выбираем атрибут текущего дня
day_today = datetime.now().day

# Создаем объект текущей даты, выбираем атрибут текущего дня
day_today = datetime.now().day

with sqlite3.connect("db/calendar.db") as con:
    cur = con.cursor()
    # Ищем в столбце date полное совпадение day_today
    cur.execute(
        "SELECT date, event FROM monthly_reminders WHERE date = ?",
        (day_today,),
    )
    # На выходе получаем список кортежей(дата, событие)
    result = cur.fetchall()

if result:
    text = f"Сегодня {day_today} число:\n"

    for _, event in result:
        text += f"{event}\n"

    print(text)
