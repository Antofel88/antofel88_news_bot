import requests
from bs4 import BeautifulSoup
import time
import random
import sqlite3
from datetime import datetime

from aiogram import F, Router
from aiogram.types import CallbackQuery

# Создаем объект текущей даты, переводим ее в строку с нужным форматом
day_today = datetime.now().strftime("%d.%m")

with sqlite3.connect("db/calendar.db") as con:
    cur = con.cursor()
    # Ищем в столбце date полное совпадение day_today
    cur.execute(
        "SELECT date, time, event FROM onetime_reminders WHERE date = ?",
        (day_today,),  # Точное совпадение
    )
    # На выходе получаем список кортежей(дата, событие)
    result = cur.fetchall()

    if result:
        text = f"Сегодня {day_today}:\n"

        for _, time_event, event in result:
            text += f"{time_event.ljust(5)} - {event}\n"       

        # Удаляем найденные записи
        cur.execute("DELETE FROM onetime_reminders WHERE date = ?", (day_today,))
