import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.inline_keyboards import traktor_kb_builder


router = Router()

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}


# Трактор
@router.callback_query(F.data == "traktor")
async def process_traktor(callback: CallbackQuery):

    await callback.message.edit_text(
        text="🖤 Трактор",
        reply_markup=traktor_kb_builder.as_markup(),
    )


@router.callback_query(F.data == "traktor_next_game")
async def process_traktor_upcoming_game(callback: CallbackQuery):
    # Создаем объект сегодняшней даты и переводим его в строку
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    # Подключение к базе данных (или создание, если её нет)
    with sqlite3.connect("db/calendar.db") as con:
        cursor = con.cursor()
        # Запрос для поиска ближайшего события
        cursor.execute(
            """
        SELECT date, team, home_guest
        FROM traktor_calendar 
        WHERE date >= ?
        ORDER BY date
        LIMIT 1
        """,
            (current_date,),
        )

        # Получение результата
        result = cursor.fetchone()

    if result:
        event_date, team, home_guest = result

        if home_guest == "дома":
            text = f"{event_date} Трактор - {team}"
        else:
            text = f"{event_date} {team} - Трактор"

        await callback.message.edit_text(
            text=text,
            reply_markup=traktor_kb_builder.as_markup(),
        )
    else:
        await callback.message.edit_text(
            text="Ближайших событий не найдено.",
            reply_markup=traktor_kb_builder.as_markup(),
        )


@router.callback_query(F.data == "khl_table")
async def process_khl_table(callback: CallbackQuery):
    url = "https://www.sports.ru/hockey/tournament/khl/table/"
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    west_table_body = soup.find_all({"class": "stat-table", "tbody": ""})
    west_teams = west_table_body[0].find_all("tr")
    east_table_body = soup.find_all({"class": "stat-table", "tbody": ""})
    east_teams = east_table_body[1].find_all("tr")

    text = "Западная конференция:\n\n"
    text += f"                    {"М".ljust(3)} {"О".ljust(3)}\n"
    for item in west_teams:
        text += f"{item.text.split("\n")[1].ljust(2)}{item.text.split("\n")[2].ljust(17)}{item.text.split("\n")[3].ljust(3)} {item.text.split("\n")[8].ljust(3)}\n"

    text += "\nВосточная конференция:\n\n"
    text += f"                    {"М".ljust(3)} {"О".ljust(3)}\n"

    for item in east_teams:
        text += f"{item.text.split("\n")[1].ljust(2)}{item.text.split("\n")[2].ljust(17)}{item.text.split("\n")[3].ljust(3)} {item.text.split("\n")[8].ljust(3)}\n"

    if callback.message.text != text:
        await callback.message.edit_text(
            text=f"`{text}`",
            reply_markup=traktor_kb_builder.as_markup(),
            parse_mode="MarkdownV2",
        )
    else:
        await callback.answer()
