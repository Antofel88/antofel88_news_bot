import requests
from bs4 import BeautifulSoup
import time
import random
import sqlite3
from datetime import datetime

from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.inline_keyboards import (
    reminders_kb_builder,
    monthly_reminders_kb_builder,
    annual_reminders_kb_builder,
    onetime_reminders_kb_builder,
)


router = Router()

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}


# Напоминания
@router.callback_query(F.data == "reminders")
async def process_reminders(callback: CallbackQuery):

    await callback.message.edit_text(
        text="📅 Напоминания",
        reply_markup=reminders_kb_builder.as_markup(),
    )


@router.callback_query(F.data == "monthly_reminders")
async def process_monthly_reminders(callback: CallbackQuery):

    await callback.message.edit_text(
        text="📅 Ежемесячные напоминания",
        reply_markup=monthly_reminders_kb_builder.as_markup(),
    )


@router.callback_query(F.data == "annual_reminders")
async def process_annual_reminders(callback: CallbackQuery):

    await callback.message.edit_text(
        text="📅 Ежегодные Напоминания",
        reply_markup=annual_reminders_kb_builder.as_markup(),
    )


@router.callback_query(F.data == "onetime_reminders")
async def process_monthly_reminders(callback: CallbackQuery):

    await callback.message.edit_text(
        text="📅 Одноразовые напоминания",
        reply_markup=onetime_reminders_kb_builder.as_markup(),
    )


@router.callback_query(F.data == "monthly_reminders_read")
async def process_monthly_reminders_read(callback: CallbackQuery):

    with sqlite3.connect("db/calendar.db") as con:
        cursor = con.cursor()
        # Выбираем все строки таблицы
        cursor.execute(
            """
            SELECT date, event 
            FROM monthly_reminders            
            ORDER BY CAST(SUBSTR(date, 1, 2) AS INTEGER)
            """
        )
        # Получение результата всех строк fetchall()
        result = cursor.fetchall()

    if result:
        text = "📅 <b>ВСЕ ЕЖЕМЕСЯЧНЫЕ НАПОМИНАНИЯ</b>\n\n"
        for date, event in result:
            text += f"{date.ljust(2)} число - {event}\n\n"

        text += f"\n📊 <b>Всего записей: {len(result)}</b>"

        await callback.message.edit_text(
            text=text,
            reply_markup=monthly_reminders_kb_builder.as_markup(),
            parse_mode="HTML",
        )
    else:
        # Если записей нет
        await callback.message.edit_text(
            text="📭 <b>Событий нет</b>\n\nБаза данных ежемесячных напоминаний пуста.",
            reply_markup=monthly_reminders_kb_builder.as_markup(),
            parse_mode="HTML",
        )


@router.callback_query(F.data == "annual_reminders_read")
async def process_annual_reminders_read(callback: CallbackQuery):

    with sqlite3.connect("db/calendar.db") as con:
        cursor = con.cursor()
        # Выбираем все строки таблицы
        cursor.execute(
            """
            SELECT date, event 
            FROM annual_reminders 
            ORDER BY 
                CAST(SUBSTR(date, 4, 2) AS INTEGER),  -- сначала по месяцу
                CAST(SUBSTR(date, 1, 2) AS INTEGER)   -- потом по дню
        """
        )
        # Получение результата всех строк fetchall()
        result = cursor.fetchall()

    if result:
        # =========================================================
        # ФОРМИРУЕМ ТЕКСТ С ГРУППИРОВКОЙ ПО МЕСЯЦАМ
        # =========================================================

        # Словарь для преобразования номера месяца в название
        month_names = {
            "01": "Январь",
            "02": "Февраль",
            "03": "Март",
            "04": "Апрель",
            "05": "Май",
            "06": "Июнь",
            "07": "Июль",
            "08": "Август",
            "09": "Сентябрь",
            "10": "Октябрь",
            "11": "Ноябрь",
            "12": "Декабрь",
        }

        text = "📅 <b>ВСЕ ЕЖЕГОДНЫЕ НАПОМИНАНИЯ</b>\n\n"

        # Переменная для отслеживания текущего месяца
        current_month = ""

        # Перебираем все отсортированные записи
        for date, event in result:
            # Извлекаем месяц из даты (последние 2 символа после точки)
            month = date.split(".")[1]  # например "15.06" -> "06"

            # Если месяц сменился, добавляем заголовок
            if month != current_month:
                # Добавляем название нового месяца
                text += f"\n<b>📌 {month_names[month]}</b>\n"
                text += "─────────────────\n"
                current_month = month

            # Добавляем само событие с отступом
            # date.ljust(5) - выравниваем дату по левому краю до 5 символов
            text += f"  ▫️ {date.ljust(5)} - {event}\n"

        # Добавляем статистику в конец
        text += f"\n📊 <b>Всего записей: {len(result)}</b>"

        await callback.message.edit_text(
            text=text,
            reply_markup=annual_reminders_kb_builder.as_markup(),
            parse_mode="HTML",
        )
    else:
        # Если записей нет
        await callback.message.edit_text(
            text="📭 <b>Событий нет</b>\n\nБаза данных ежегодных напоминаний пуста.",
            reply_markup=annual_reminders_kb_builder.as_markup(),
            parse_mode="HTML",
        )


@router.callback_query(F.data == "annual_reminders_current_month")
async def process_annual_reminders_current_month(callback: CallbackQuery):

    day_today = datetime.now().strftime("%m")

    with sqlite3.connect("db/calendar.db") as con:
        cur = con.cursor()
        cur.execute(
            """
            SELECT date, event 
            FROM annual_reminders 
            WHERE date LIKE ? 
            ORDER BY CAST(SUBSTR(date, 1, 2) AS INTEGER)
            """,
            (f"%.{day_today}",),
        )
        result = cur.fetchall()

    if result:
        # Словарь для преобразования номера месяца в название
        month_names = {
            "01": "Январь",
            "02": "Февраль",
            "03": "Март",
            "04": "Апрель",
            "05": "Май",
            "06": "Июнь",
            "07": "Июль",
            "08": "Август",
            "09": "Сентябрь",
            "10": "Октябрь",
            "11": "Ноябрь",
            "12": "Декабрь",
        }

        text = f"📅 <b>{month_names[day_today]}</b>\n\n"

        for date, event in result:
            text += f"{date.ljust(5)} - {event}\n\n"

        await callback.message.edit_text(
            text=text,
            reply_markup=annual_reminders_kb_builder.as_markup(),
            parse_mode="HTML",
        )
    else:
        # Если записей нет
        await callback.message.edit_text(
            text="📭 <b>В этом месяце событий нет</b>\n\n",
            reply_markup=annual_reminders_kb_builder.as_markup(),
            parse_mode="HTML",
        )


@router.callback_query(F.data == "onetime_reminders_current_month")
async def process_onetime_reminders_current_month(callback: CallbackQuery):

    day_today = datetime.now().strftime("%m")

    with sqlite3.connect("db/calendar.db") as con:
        cur = con.cursor()
        cur.execute(
            """
            SELECT date, time, event 
            FROM onetime_reminders 
            WHERE date LIKE ? 
            ORDER BY CAST(SUBSTR(date, 1, 2) AS INTEGER)
            """,
            (f"%.{day_today}",),
        )
        result = cur.fetchall()

    if result:
        # Словарь для преобразования номера месяца в название
        month_names = {
            "01": "Январь",
            "02": "Февраль",
            "03": "Март",
            "04": "Апрель",
            "05": "Май",
            "06": "Июнь",
            "07": "Июль",
            "08": "Август",
            "09": "Сентябрь",
            "10": "Октябрь",
            "11": "Ноябрь",
            "12": "Декабрь",
        }

        text = f"📅 <b>{month_names[day_today]}</b>\n\n"

        for date, time_event, event in result:
            text += f"{date.ljust(5)} {time_event.ljust(5)} - {event}\n\n"

        await callback.message.edit_text(
            text=text,
            reply_markup=annual_reminders_kb_builder.as_markup(),
            parse_mode="HTML",
        )
    else:
        # Если записей нет
        await callback.message.edit_text(
            text="📭 <b>В этом месяце событий нет</b>\n\n",
            reply_markup=annual_reminders_kb_builder.as_markup(),
            parse_mode="HTML",
        )


@router.callback_query(F.data == "onetime_reminders_read")
async def process_onetime_reminders_read(callback: CallbackQuery):

    with sqlite3.connect("db/calendar.db") as con:
        cursor = con.cursor()
        # Выбираем все строки таблицы
        cursor.execute(
            """
            SELECT date, time, event 
            FROM onetime_reminders 
            ORDER BY 
                CAST(SUBSTR(date, 4, 2) AS INTEGER),  -- сначала по месяцу
                CAST(SUBSTR(date, 1, 2) AS INTEGER)   -- потом по дню
        """
        )
        # Получение результата всех строк fetchall()
        result = cursor.fetchall()

    if result:
        # =========================================================
        # ФОРМИРУЕМ ТЕКСТ С ГРУППИРОВКОЙ ПО МЕСЯЦАМ
        # =========================================================

        # Словарь для преобразования номера месяца в название
        month_names = {
            "01": "Январь",
            "02": "Февраль",
            "03": "Март",
            "04": "Апрель",
            "05": "Май",
            "06": "Июнь",
            "07": "Июль",
            "08": "Август",
            "09": "Сентябрь",
            "10": "Октябрь",
            "11": "Ноябрь",
            "12": "Декабрь",
        }

        text = "📅 <b>ВСЕ ЕЖЕГОДНЫЕ НАПОМИНАНИЯ</b>\n\n"

        # Переменная для отслеживания текущего месяца
        current_month = ""

        # Перебираем все отсортированные записи
        for date, time_event, event in result:
            # Извлекаем месяц из даты (последние 2 символа после точки)
            month = date.split(".")[1]  # например "15.06" -> "06"

            # Если месяц сменился, добавляем заголовок
            if month != current_month:
                # Добавляем название нового месяца
                text += f"\n<b>📌 {month_names[month]}</b>\n"
                text += "─────────────────\n"
                current_month = month

            # Добавляем само событие с отступом
            # date.ljust(5) - выравниваем дату по левому краю до 5 символов
            text += f"  ▫️ {date.ljust(5)} {time_event.ljust(5)} - {event}\n"

        # Добавляем статистику в конец
        text += f"\n📊 <b>Всего записей: {len(result)}</b>"

        await callback.message.edit_text(
            text=text,
            reply_markup=annual_reminders_kb_builder.as_markup(),
            parse_mode="HTML",
        )
    else:
        # Если записей нет
        await callback.message.edit_text(
            text="📭 <b>Событий нет</b>\n\nБаза данных одноразовых напоминаний пуста.",
            reply_markup=annual_reminders_kb_builder.as_markup(),
            parse_mode="HTML",
        )
