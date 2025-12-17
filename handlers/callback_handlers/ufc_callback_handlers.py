import requests
from bs4 import BeautifulSoup
import time
import random

from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.inline_keyboards import ufc_kb_builder


router = Router()

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}


# UFC
@router.callback_query(F.data == "ufc")
async def process_ufc(callback: CallbackQuery):
    await callback.message.edit_text(
        text="🥊 UFC",
        reply_markup=ufc_kb_builder.as_markup(),
    )


@router.callback_query(F.data == "ufc_next_tournament")
async def process_ufc_upcoming_tournament(callback: CallbackQuery):
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

    if callback.message.text != text:
        await callback.message.edit_text(
            text=text,
            reply_markup=ufc_kb_builder.as_markup(),
        )
    else:
        await callback.answer()
