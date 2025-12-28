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
)


router = Router()

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}


# Вывод клавы напоминаний
@router.callback_query(F.data == "reminders_kb")
async def process_reminders_kb(callback: CallbackQuery):

    await callback.message.edit_text(
        text="📅 Напоминания",
        reply_markup=reminders_kb_builder.as_markup(),
    )


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


@router.callback_query(F.data == "monthly_reminders_read")
async def process_monthly_reminders_read(callback: CallbackQuery):

    with sqlite3.connect("db/calendar.db") as con:
        cursor = con.cursor()
        # Выбираем все строки таблицы
        cursor.execute("SELECT * FROM monthly_reminders")
        # Получение результата всех строк fetchall()
        result = cursor.fetchall()

    if result:
        text = ""
        for num, date, event in result:
            text += f"{str(num).ljust(2)}| {date.ljust(2)} число - {event}\n\n"

        await callback.message.edit_text(
            text=f"`{text}`",
            reply_markup=monthly_reminders_kb_builder.as_markup(),
            parse_mode="MarkdownV2",
        )
    else:
        await callback.message.edit_text(
            text="Событий нет.",
            reply_markup=monthly_reminders_kb_builder.as_markup(),
        )


@router.callback_query(F.data == "annual_reminders_read")
async def process_annual_reminders_read(callback: CallbackQuery):

    with sqlite3.connect("db/calendar.db") as con:
        cursor = con.cursor()
        # Выбираем все строки таблицы
        cursor.execute("SELECT * FROM annual_reminders")
        # Получение результата всех строк fetchall()
        result = cursor.fetchall()

    if result:
        text = ""
        for num, date, event in result:
            text += f"{str(num).ljust(3)}| {date.ljust(5)} - {event}\n\n"

        await callback.message.edit_text(
            text=f"`{text}`",
            reply_markup=annual_reminders_kb_builder.as_markup(),
            parse_mode="MarkdownV2",
        )
    else:
        await callback.message.edit_text(
            text="Событий нет.",
            reply_markup=annual_reminders_kb_builder.as_markup(),
        )

