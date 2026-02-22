from aiogram import Bot
import sqlite3

import requests
from bs4 import BeautifulSoup

import time
from datetime import date
from datetime import datetime, timedelta

import random
import re


# Создаем объект текущей даты, переводим ее в строку с нужным форматом и убираем нули в днях
day_today = datetime.now().strftime("%d.%m")

with sqlite3.connect("db/calendar.db") as con:
    cur = con.cursor()
    # Ищем в столбце date полное совпадение day_today
    cur.execute(
        "SELECT date, event FROM annual_reminders WHERE date = ?",
        (day_today,),  # Точное совпадение
    )
    # На выходе получаем список кортежей(дата, событие)
    result = cur.fetchall()

if result:
    text = f"Сегодня {day_today}:\n"

    for _, event in result:
        text += f"{event}\n"

    print