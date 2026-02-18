from aiogram import Bot
import sqlite3

import requests
from bs4 import BeautifulSoup

import time
from datetime import date
from datetime import datetime, timedelta

import random
import re

url = "https://www.bloodandsweat.ru/events_types/ufc/"
response = requests.get(url=url)

soup = BeautifulSoup(response.text, "lxml")

ufc_name = soup.find(class_="list-block-item").find("h2").text
ufc_date = soup.find(class_="content-text-p").find("span").find_next("span").text

ufc_card_link = soup.find(class_="list-block-text").find("a").get("href")

time.sleep(random.uniform(0.512, 1.356))
response = requests.get(url=ufc_card_link)
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

ufc_date_list = [18, 3]
print(ufc_date_list[0])

# Делаем проверку на сегодня, ближайшие два дня и еще переход на первые дни месяца, т.к. 30+2=32, а такого дня в месяце нет
if (
    (day_today == ufc_date_list[0])
    or ((day_today + 1) == ufc_date_list[0])
    or ((day_today + 2) == ufc_date_list[0])
    or (1 == ufc_date_list[0])
    or (2 == ufc_date_list[0])
):
    print(text)
