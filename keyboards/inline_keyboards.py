from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Создаем объект билдера
main_kb_builder = InlineKeyboardBuilder()
# Создаем список с инлайн-кнопками для главной клавиатуры
main_inline_buttons = [
    InlineKeyboardButton(
        text="🖤 Трактор",
        callback_data="traktor",
    ),
    InlineKeyboardButton(
        text="🥊 UFC",
        callback_data="ufc",
    ),
    InlineKeyboardButton(text="🏎 F1", callback_data="f1"),
    InlineKeyboardButton(text="📅 Напоминания", callback_data="reminders"),
]
# Распаковываем список с кнопками в билдер, указываем, что в одном ряду должна быть 1 кнопка
main_kb_builder.row(*main_inline_buttons, width=1)

# Трактор
traktor_kb_builder = InlineKeyboardBuilder()
traktor_inline_buttons = [
    InlineKeyboardButton(text="Ближайшая игра", callback_data="traktor_next_game"),
    InlineKeyboardButton(text="Таблица КХЛ", callback_data="khl_table"),
    InlineKeyboardButton(
        text="Вся статистика",
        url="https://www.flashscorekz.com/team/tractor-chelyabinsk/C2PzG534/",
    ),
    InlineKeyboardButton(text="Трансляция ОТВ", url="https://1obl.tv/online/"),
    InlineKeyboardButton(
        text="Трансляция КП", url="https://hd.kinopoisk.ru/sport/team/80838/"
    ),
    InlineKeyboardButton(
        text="На главную",
        callback_data="main_kb",
    ),
]
traktor_kb_builder.row(*traktor_inline_buttons, width=1)

# UFC
ufc_kb_builder = InlineKeyboardBuilder()
ufc_inline_buttons = [
    InlineKeyboardButton(
        text="Ближайший турнир",
        callback_data="ufc_next_tournament",
    ),
    InlineKeyboardButton(
        text="Полное расписание",
        url="https://www.bloodandsweat.ru/events_types/ufc/",
    ),
    InlineKeyboardButton(
        text="Новости",
        url="https://fighttime.ru/",
    ),
    InlineKeyboardButton(
        text="Трансляция МАТЧ ТВ",
        url="https://matchtv.ru/on-air",
    ),
    InlineKeyboardButton(
        text="Трансляция КП",
        url="https://hd.kinopoisk.ru/sport/competition/114468",
    ),
    InlineKeyboardButton(
        text="На главную",
        callback_data="main_kb",
    ),
]
ufc_kb_builder.row(*ufc_inline_buttons, width=1)

# F1
f1_kb_builder = InlineKeyboardBuilder()
f1_inline_buttons = [
    InlineKeyboardButton(
        text="Ближайшая гонка",
        callback_data="f1_next_race",
    ),
    InlineKeyboardButton(text="Таблица", callback_data="f1_table"),
    InlineKeyboardButton(
        text="Полное расписание",
        callback_data="f1_calendar",
    ),
    InlineKeyboardButton(
        text="Новости",
        url="https://www.championat.com/auto/_f1.html",
    ),
    InlineKeyboardButton(
        text="Трансляция VK", url="https://vkvideo.ru/@stanizlavskylive"
    ),
    InlineKeyboardButton(
        text="На главную",
        callback_data="main_kb",
    ),
]
f1_kb_builder.row(*f1_inline_buttons, width=1)

# Напоминания
reminders_kb_builder = InlineKeyboardBuilder()
reminders_inline_buttons = [
    InlineKeyboardButton(
        text="Ежемесячные напоминания",
        callback_data="monthly_reminders",
    ),
    InlineKeyboardButton(
        text="Ежегодные напоминания", callback_data="annual_reminders"
    ),
    InlineKeyboardButton(
        text="Одноразовые напоминания", callback_data="onetime_reminders"
    ),
    InlineKeyboardButton(
        text="На главную",
        callback_data="main_kb",
    ),
]
reminders_kb_builder.row(*reminders_inline_buttons, width=1)

monthly_reminders_kb_builder = InlineKeyboardBuilder()
monthly_reminders_inline_buttons = [
    InlineKeyboardButton(
        text="Все напоминания",
        callback_data="monthly_reminders_read",
    ),
    InlineKeyboardButton(
        text="Добавить",
        callback_data="monthly_reminders_write",
    ),
    InlineKeyboardButton(
        text="Удалить",
        callback_data="monthly_reminders_delete",
    ),
    InlineKeyboardButton(
        text="Назад",
        callback_data="reminders",
    ),
]
monthly_reminders_kb_builder.row(*monthly_reminders_inline_buttons, width=1)

annual_reminders_kb_builder = InlineKeyboardBuilder()
annual_reminders_inline_buttons = [
    InlineKeyboardButton(
        text="Все напоминания",
        callback_data="annual_reminders_read",
    ),
    InlineKeyboardButton(
        text="Текущий месяц",
        callback_data="annual_reminders_current_month",
    ),
    InlineKeyboardButton(
        text="Добавить",
        callback_data="annual_reminders_write",
    ),
    InlineKeyboardButton(
        text="Удалить",
        callback_data="annual_reminders_delete",
    ),
    InlineKeyboardButton(
        text="Назад",
        callback_data="reminders",
    ),
]
annual_reminders_kb_builder.row(*annual_reminders_inline_buttons, width=1)

onetime_reminders_kb_builder = InlineKeyboardBuilder()
onetime_reminders_inline_buttons = [
    InlineKeyboardButton(
        text="Все напоминания",
        callback_data="onetime_reminders_read",
    ),
    InlineKeyboardButton(
        text="Текущий месяц",
        callback_data="onetime_reminders_current_month",
    ),
    InlineKeyboardButton(
        text="Добавить",
        callback_data="onetime_reminders_write",
    ),
    InlineKeyboardButton(
        text="Удалить",
        callback_data="onetime_reminders_delete",
    ),
    InlineKeyboardButton(
        text="Назад",
        callback_data="reminders",
    ),
]
onetime_reminders_kb_builder.row(*onetime_reminders_inline_buttons, width=1)
