from aiogram import Router
from aiogram.types import Message


router = Router()


# Хэндлер для сообщений, которые не попали в другие хэндлеры
# @router.message()
# async def process_other_answer(message: Message):
#     await message.answer("Я умею реагировать только на кнопки клавиатуры и команды.")
