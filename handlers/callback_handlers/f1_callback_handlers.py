import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.inline_keyboards import f1_kb_builder


router = Router()

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}


# F1
@router.callback_query(F.data == "f1")
async def process_f1(callback: CallbackQuery):

    await callback.message.edit_text(
        text="🏎 F1",
        reply_markup=f1_kb_builder.as_markup(),
    )


@router.callback_query(F.data == "f1_next_race")
async def process_f1_next_race(callback: CallbackQuery):

    # Создаем объект сегодняшней даты и переводим его в строку
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    # Подключение к базе данных (или создание, если её нет)
    with sqlite3.connect("db/calendar.db") as con:
        cursor = con.cursor()
        # Запрос для поиска ближайшего события
        cursor.execute(
            """
        SELECT date, event
        FROM f1_calendar 
        WHERE date >= ?
        ORDER BY date
        LIMIT 1
        """,
            (current_date,),
        )

        # Получение результата
        result = cursor.fetchone()

    if result:
        event_date, race = result
        text = f"{event_date} {race}"

        await callback.message.edit_text(
            text=text,
            reply_markup=f1_kb_builder.as_markup(),
        )
    else:
        await callback.message.edit_text(
            text="Ближайших гонок не найдено.",
            reply_markup=f1_kb_builder.as_markup(),
        )


@router.callback_query(F.data == "f1_table")
async def process_f1_table(callback: CallbackQuery):
    url = "https://www.sports.ru/automoto/tournament/f1-championship/table/"
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    name = soup.find(class_="stat mB6").find("tbody").find_all("tr")
    team = (
        soup.find(class_="stat mB6")
        .next_sibling.next_sibling.next_sibling.next_sibling.find("tbody")
        .find_all("tr")
    )
    text = ""

    text += "Личный зачёт:\n\n"
    for index, item in enumerate(name, start=1):
        text += f"{str(index).ljust(2)} {item.find(class_="name-td alLeft bordR").text.strip().ljust(22)} {item.find(class_="name-td alLeft bordR").next_sibling.next_sibling.next_sibling.next_sibling.text.rjust(3)}\n"

    text += "\nКубок конструкторов:\n\n"
    for index, item in enumerate(team, start=1):
        text += f"{str(index).ljust(2)} {item.find(class_="name-td alLeft bordR").text.strip().ljust(22)} {item.find(class_="name-td alLeft bordR").next_sibling.next_sibling.text.rjust(3)}\n"

    if callback.message.text != text:
        await callback.message.edit_text(
            text=f"`{text}`",
            reply_markup=f1_kb_builder.as_markup(),
            parse_mode="MarkdownV2",
        )
    else:
        await callback.answer()


@router.callback_query(F.data == "f1_calendar")
async def process_f1_calendar(callback: CallbackQuery):
    with sqlite3.connect("db/calendar.db") as con:
        cursor = con.cursor()
        # Выбираем все строки таблицы
        cursor.execute("SELECT * FROM f1_calendar")
        # Получение результата всех строк fetchall()
        result = cursor.fetchall()

    if result:
        text = ""
        for date, event in result:
            text += f"{date.ljust(5)} {event}\n\n"

        await callback.message.edit_text(
            text=f"`{text}`",
            reply_markup=f1_kb_builder.as_markup(),
            parse_mode="MarkdownV2",
        )
    else:
        await callback.message.edit_text(
            text="Событий нет.",
            reply_markup=f1_kb_builder.as_markup(),
        )
