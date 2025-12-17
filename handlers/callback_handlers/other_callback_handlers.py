from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.inline_keyboards import main_kb_builder


router = Router()

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}


# Вызов главной клавиатуры
@router.callback_query(F.data == "main_kb")
async def process_traktor(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Новости",
        reply_markup=main_kb_builder.as_markup(),
    )
