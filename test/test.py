from aiogram import F, Router  # F - для фильтров, Router - для создания маршрутизатора
from aiogram.types import CallbackQuery, Message  # Типы сообщений
from aiogram.fsm.context import (
    FSMContext,
)  # Контекст для работы с FSM (Finite State Machine)
from aiogram.fsm.state import State, StatesGroup  # Классы для создания состояний
import sqlite3  # Для работы с SQLite базой данных

# Создаем роутер - объект для группировки обработчиков
router = Router()


# СОЗДАЕМ КЛАСС СОСТОЯНИЙ (STATESGROUP)
# StatesGroup - это класс, который группирует связанные состояния
# Наследование от StatesGroup позволяет aiogram автоматически регистрировать состояния
class AddMonthlyReminder(StatesGroup):
    """
    Класс состояний для процесса добавления напоминания.
    Каждое состояние - это отдельный этап диалога с пользователем.
    """

    # State() создает объект состояния
    date = State()  # Состояние 1: ожидание ввода числа (даты)
    event = State()  # Состояние 2: ожидание ввода события (текста)


# ОБРАБОТЧИК НАЖАТИЯ НА КНОПКУ "Добавить" (НАЧАЛО ПРОЦЕССА)
@router.callback_query(F.data == "monthly_reminders_write")
async def add_reminder_start(callback: CallbackQuery, state: FSMContext):
    """
    Эта функция вызывается когда пользователь нажимает на inline-кнопку
    с callback_data="monthly_reminders_write"

    Параметры:
    - callback: CallbackQuery - информация о нажатии кнопки
    - state: FSMContext - объект для управления состоянием пользователя
    """

    # Отправляем пользователю сообщение с просьбой ввести число
    await callback.message.answer("Введите число:")

    # Устанавливаем начальное состояние для этого пользователя
    # set_state() переводит пользователя в указанное состояние
    # Теперь все сообщения от этого пользователя будут проверяться на соответствие этому состоянию
    await state.set_state(AddMonthlyReminder.date)


# ОБРАБОТЧИК ВВОДА ДАТЫ (ПЕРВЫЙ ШАГ)
@router.message(AddMonthlyReminder.date)
async def save_date_monthly_reminders(message: Message, state: FSMContext):
    """
    Эта функция вызывается когда:
    1. Пользователь отправил текстовое сообщение
    2. ТЕКУЩЕЕ состояние пользователя = AddReminder.date

    Функция получает число от пользователя и переводит его к следующему шагу
    """
    # Сохраняем введенное число во временное хранилище FSM
    # update_data() добавляет или обновляет данные в хранилище состояний
    # Эти данные будут доступны на следующих шагах
    await state.update_data(date=message.text)

    # Меняем состояние пользователя на следующее
    # Теперь будем ждать ввод события
    await state.set_state(AddMonthlyReminder.event)

    # Просим пользователя ввести событие
    await message.answer("Введите событие:")


# ОБРАБОТЧИК ВВОДА СОБЫТИЯ (ВТОРОЙ ШАГ И СОХРАНЕНИЕ В БД)
@router.message(AddMonthlyReminder.event)
async def save_event_monthly_reminders(message: Message, state: FSMContext):
    """
    Эта функция вызывается когда:
    1. Пользователь отправил текстовое сообщение
    2. ТЕКУЩЕЕ состояние пользователя = ddMonthlyReminder.event

    Функция получает событие и сохраняет все данные в базу данных
    """

    # Получаем все сохраненные данные из хранилища FSM
    # get_data() возвращает словарь со всеми данными, которые мы сохранили через update_data()
    data = await state.get_data()

    # Извлекаем дату из полученных данных
    # data['date'] - это число, которое пользователь ввел на предыдущем шаге
    date = data["date"]

    # message.text - это текст события, которое пользователь ввел сейчас
    event = message.text

    # СОХРАНЕНИЕ В БАЗУ ДАННЫХ SQLite
    # Используем контекстный менеджер (with) для работы с базой данных
    # Контекстный менеджер автоматически:
    # 1. Открывает соединение с БД
    # 2. При успешном завершении блока - делает commit (сохраняет изменения)
    # 3. При ошибке - делает rollback (откатывает изменения)
    # 4. Закрывает соединение с БД
    with sqlite3.connect("db/calendar.db") as conn:

        # Создаем таблицу если она не существует
        # IF NOT EXISTS гарантирует, что таблица создастся только если ее еще нет
        conn.execute(
            "CREATE TABLE IF NOT EXISTS monthly_reminders (date TEXT, event TEXT)"
        )

        # Вставляем данные в таблицу
        # ? - placeholders для защиты от SQL-инъекций
        # (date, event) - кортеж значений, которые подставятся вместо ?
        conn.execute(
            "INSERT INTO monthly_reminders VALUES (date, event)", (date, event)
        )
        # commit() вызывается автоматически при выходе из блока with

    # ЗАВЕРШЕНИЕ ПРОЦЕССА
    # Очищаем состояние пользователя
    # clear() удаляет все данные из хранилища FSM для этого пользователя
    # Пользователь возвращается в "нейтральное" состояние
    await state.clear()
    await message.answer(f"Событие {date} {event} успешно добавлено в БД")
