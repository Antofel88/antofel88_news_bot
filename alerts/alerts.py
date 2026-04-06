from aiogram import Bot
import sqlite3

import requests
from bs4 import BeautifulSoup

import time
from datetime import date
from datetime import datetime, timedelta

import random
import re

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}


async def traktor_next_game_alert(bot: Bot):

    # Создаем объект сегодняшней даты и переводим его в строку
    day_today = datetime.now().strftime("%Y-%m-%d")

    with sqlite3.connect("db/calendar.db") as con:
        cur = con.cursor()
        cur.execute(
            "SELECT date, team, home_guest FROM traktor_calendar WHERE date LIKE ?",
            (f"{day_today}%",),
        )
        result = cur.fetchall()[0]  # т.к. кортеж в списке

    if result:
        date, team, home_guest = result

        chat_ids = ["951807751", "749731969"]  # список с чатами, второй - Санин

        for chat_id in chat_ids:

            if home_guest == "дома":
                text = f"Сегодня {date} Трактор - {team}\n\nТрансляция ОТВ: https://1obl.tv/online\nТрансляция КП: https://hd.kinopoisk.ru/sport/team/80838"
            else:
                text = f"Сегодня {date} {team} - Трактор\n\nТрансляция ОТВ: https://1obl.tv/online\nТрансляция КП: https://hd.kinopoisk.ru/sport/team/80838"

            await bot.send_message(chat_id=chat_id, text=text)


async def ufc_next_tournament_alert(bot: Bot):

    url = "https://www.bloodandsweat.ru/events_types/ufc/"
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    ufc_name = soup.find(class_="list-block-item").find("h2").text
    ufc_date = soup.find(class_="content-text-p").find("span").find_next("span").text
    ufc_card_link = soup.find(class_="list-block-text").find("a").get("href")

    time.sleep(random.uniform(0.512, 1.356))
    response = requests.get(url=ufc_card_link, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    ufc_card = soup.find(class_="entry-content").find_all("strong")

    text = f"{ufc_name}\n{ufc_date}\n"

    for item in ufc_card:
        if item.next_sibling:
            text += f"{item.text}{item.next_sibling.text}\n"
        else:
            text += f"\n{item.text}\n\n"

    text += "\n\nТрансляция МАТЧ ТВ: https://matchtv.ru/on-air \nТрансляция КП: https://hd.kinopoisk.ru/sport/competition/114468"
    day_today = date.today().day
    # Получаем список в формате [дата, год]
    ufc_date_list = list(map(int, re.findall(r"\b\d+\b", ufc_date)))
    # Делаем проверку на ближайшие два дня и еще переход на первые дни месяца, т.к. 30+2=32, а такого дня в месяце нет
    if (
        (day_today == ufc_date_list[0])
        or ((day_today + 1) == ufc_date_list[0])
        or ((day_today + 2) == ufc_date_list[0])
        or (1 == ufc_date_list[0])
        or (2 == ufc_date_list[0])
    ):
        await bot.send_message(
            chat_id="951807751",
            text=text,
        )


async def f1_next_race_alert(bot: Bot):

    today = datetime.now()
    tomorrow = (today + timedelta(days=1)).strftime("%Y-%m-%d")

    with sqlite3.connect("db/calendar.db") as con:
        cur = con.cursor()
        cur.execute(
            "SELECT date, event FROM f1_calendar WHERE date LIKE ?",
            (f"{tomorrow}%",),
        )

        result = cur.fetchall()[0]  # т.к. кортеж в списке

    if result:
        date, event = result

        chat_ids = ["951807751", "749731969"]  # список с чатами, второй - Санин

        for chat_id in chat_ids:

            await bot.send_message(
                chat_id=chat_id,
                text=f"Завтра {date} {event}\n\nТрансляция VK: https://vkvideo.ru/@stanizlavskylive",
            )


async def monthly_reminders_alert(bot: Bot):

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

        await bot.send_message(
            chat_id="951807751",
            text=text,
        )


async def annual_reminders_alert(bot: Bot):

    # Создаем объект текущей даты, переводим ее в строку с нужным форматом
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

        await bot.send_message(
            chat_id="951807751",
            text=text,
        )


async def onetime_reminders_alert(bot: Bot):

    # Создаем объект текущей даты и времени, переводим ее в строку с нужным форматом
    now = datetime.now() + timedelta(hours=2)
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

            await bot.send_message(
                chat_id="951807751",
                text=text,
            )
            # Удаляем все отправленные напоминания
            cur.execute(
                "DELETE FROM onetime_reminders WHERE date = ? AND time <= ?",
                (day_today, current_time),
            )
