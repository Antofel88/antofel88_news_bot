from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from keyboards.inline_keyboards import main_kb_builder


router = Router()


# Этот хэндлер будет срабатывать на команду "/start"
# и отправлять в чат клавиатуру
@router.message(CommandStart())
async def process_command_start(message: Message):
    if message.from_user.id == 951807751:
        await message.answer(
            "Новости",
            reply_markup=main_kb_builder.as_markup(),
        )
