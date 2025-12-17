import requests
from bs4 import BeautifulSoup
import sqlite3 as sq
from datetime import datetime, timedelta

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}


async def traktor_update_db():
    url = "https://www.sports.ru/hockey/club/traktor/calendar/"
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    date = soup.find("tbody").find_all(class_="name-td alLeft bordR")
    team = soup.find("tbody").find_all(class_="name-td alLeft")
    score = soup.find("tbody").find_all(class_="score")
    home_guest = soup.find("tbody").find_all(class_="alRight padR20")

    date = [i for i in date if "|" in i.text]
    team = [
        i
        for i in team
        if ("КХЛ" not in i.text.upper()) and ("КУБОК ГАГАРИНА" not in i.text.upper())
    ]

    with sq.connect("db/calendar.db") as con:
        cur = con.cursor()

        cur.execute(f"""DELETE FROM traktor_calendar""")

        cur.execute(
            """CREATE TABLE IF NOT EXISTS traktor_calendar (
                    date TEXT,
                    team TEXT,
                    home_guest TEXT,
                    score TEXT
                    )"""
        )

        for item in zip(date, team, home_guest, score):
            cur.execute(
                f"""INSERT INTO traktor_calendar (date, team, home_guest, score) VALUES ("{ (
                datetime.strptime(item[0].text.strip(), "%d.%m.%Y|%H:%M")
                + timedelta(hours=2)
            ).strftime("%Y-%m-%d %H:%M")}", "{item[1].text.strip()}", "{item[2].text.strip().lower()}", "{item[3].text.strip().replace("\n", " ")}")"""
            )

async def f1_update_db():
    url = "https://www.championat.com/auto/_f1/tournament/922/calendar/"
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    date = soup.find_all(class_="tournament-calendar__date")
    race = soup.find_all(class_="tournament-calendar__name")

    with sq.connect("db/calendar.db") as con:
        cur = con.cursor()

        cur.execute(f"""DELETE FROM f1_calendar""")

        cur.execute(
            """CREATE TABLE IF NOT EXISTS f1_calendar (
                    date TEXT,
                    race TEXT
                    )"""
        )

        for item in zip(date, race):
            if "гонка" in item[1].text.lower() or (
                "спринт" in item[1].text.lower()
                and "квалификация" not in item[1].text.lower()
            ):
                cur.execute(
                    f"""INSERT INTO f1_calendar (date, race) VALUES ("{(
                    datetime.strptime(item[0].text.strip(), "%d.%m.%Y %H:%M")
                    + timedelta(hours=2)
                ).strftime("%Y-%m-%d %H:%M")}", "{item[1].text.strip()}")"""
                )

# async def washington_update_db():
#     url = "https://www.sports.ru/hockey/club/washington-capitals/calendar/"
#     response = requests.get(url=url, headers=headers)
#     soup = BeautifulSoup(response.text, "lxml")
#
#     date = soup.find("tbody").find_all(class_="name-td alLeft bordR")
#     team = soup.find("tbody").find_all(class_="name-td alLeft")
#     score = soup.find("tbody").find_all(class_="score")
#     home_guest = soup.find("tbody").find_all(class_="alRight padR20")
#
#     date = [i for i in date if "|" in i.text]
#     team = [
#         i
#         for i in team
#         if ("НХЛ" not in i.text.upper()) and ("КУБОК СТЭНЛИ" not in i.text.upper())
#     ]
#
#     with sq.connect("db/calendar.db") as con:
#         cur = con.cursor()
#
#         cur.execute(f"""DELETE FROM caps_calendar""")
#
#         cur.execute(
#             """CREATE TABLE IF NOT EXISTS caps_calendar (
#                     date TEXT,
#                     team TEXT,
#                     home_guest TEXT,
#                     score TEXT
#                     )"""
#         )
#
#         for item in zip(date, team, home_guest, score):
#             cur.execute(
#                 f"""INSERT INTO caps_calendar (date, team, home_guest, score) VALUES ("{ (
#                 datetime.strptime(item[0].text.strip(), "%d.%m.%Y|%H:%M")
#                 + timedelta(hours=2)
#             ).strftime("%Y-%m-%d %H:%M")}", "{item[1].text.strip()}", "{item[2].text.strip().lower()}", "{item[3].text.strip().replace("\n", " ")}")"""
#             )
#
# async def edmonton_update_db():
#     url = "https://www.sports.ru/hockey/club/edmonton-oilers/calendar/"
#     response = requests.get(url=url, headers=headers)
#     soup = BeautifulSoup(response.text, "lxml")
#
#     date = soup.find("tbody").find_all(class_="name-td alLeft bordR")
#     team = soup.find("tbody").find_all(class_="name-td alLeft")
#     score = soup.find("tbody").find_all(class_="score")
#     home_guest = soup.find("tbody").find_all(class_="alRight padR20")
#
#     date = [i for i in date if "|" in i.text]
#     team = [
#         i
#         for i in team
#         if ("НХЛ" not in i.text.upper()) and ("КУБОК СТЭНЛИ" not in i.text.upper())
#     ]
#
#     with sq.connect("db/calendar.db") as con:
#         cur = con.cursor()
#
#         cur.execute(f"""DELETE FROM edmonton_calendar""")
#
#         cur.execute(
#             """CREATE TABLE IF NOT EXISTS edmonton_calendar (
#                     date TEXT,
#                     team TEXT,
#                     home_guest TEXT,
#                     score TEXT
#                     )"""
#         )
#
#         for item in zip(date, team, home_guest, score):
#             cur.execute(
#                 f"""INSERT INTO edmonton_calendar (date, team, home_guest, score) VALUES ("{ (
#                 datetime.strptime(item[0].text.strip(), "%d.%m.%Y|%H:%M")
#                 + timedelta(hours=2)
#             ).strftime("%Y-%m-%d %H:%M")}", "{item[1].text.strip()}", "{item[2].text.strip().lower()}", "{item[3].text.strip().replace("\n", " ")}")"""
#             )
