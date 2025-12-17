import requests
from bs4 import BeautifulSoup
import time
import random
import sqlite3
from datetime import datetime

from aiogram import F, Router
from aiogram.types import CallbackQuery

with sqlite3.connect("db/calendar.db") as con:
    cursor = con.cursor()
    # Выбираем все строки таблицы
    cursor.execute("SELECT * FROM f1_calendar")
    # Получение результата всех строк fetchall()
    result = cursor.fetchall()

if result:
    text = "Число Событие\n\n"
    for date, event in result:
        text += f"{date.ljust(5)} {event}\n\n"

print(text)
