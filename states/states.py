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
    Класс состояний для процесса добавления ежемесячного напоминания.
    Каждое состояние - это отдельный этап диалога с пользователем.
    """

    # State() создает объект состояния
    date = State()  # Состояние 1: ожидание ввода числа (даты)
    event = State()  # Состояние 2: ожидание ввода события (текста)


class DeleteMonthlyReminder(StatesGroup):
    """
    Класс состояний для процесса удаления ежемесячного напоминания.
    Каждое состояние - это отдельный этап диалога с пользователем.
    """

    select_id = State()  # Состояние 1: ожидание ввода ID записи и удаление


class AddAnnualReminder(StatesGroup):
    """
    Класс состояний для процесса добавления ежегодного напоминания.
    Каждое состояние - это отдельный этап диалога с пользователем.
    """

    # State() создает объект состояния
    date = State()  # Состояние 1: ожидание ввода числа (даты)
    event = State()  # Состояние 2: ожидание ввода события (текста)


class DeleteAnnualReminder(StatesGroup):
    """
    Класс состояний для процесса удаления ежегодного напоминания.
    Каждое состояние - это отдельный этап диалога с пользователем.
    """

    select_id = State()  # Состояние 1: ожидание ввода ID записи и удаление


class AddOnetimeReminder(StatesGroup):
    """
    Класс состояний для процесса добавления одноразового напоминания.
    Каждое состояние - это отдельный этап диалога с пользователем.
    """

    # State() создает объект состояния
    date = State()  # Состояние 1: ожидание ввода числа (даты)
    time = State()  # Состояние 2: ожидание ввода времни (текста)
    event = State()  # Состояние 3: ожидание ввода события (текста)


class DeleteOnetimeReminder(StatesGroup):
    """
    Класс состояний для процесса удаления одноразового напоминания.
    Каждое состояние - это отдельный этап диалога с пользователем.
    """

    select_id = State()  # Состояние 1: ожидание ввода ID записи и удаление


def normalize_date(date_str: str) -> str:
    """
    Принимает дату в любом формате (д.м, дд.м, д.мм, дд.мм)
    Возвращает нормализованную дату в формате ДД.ММ
    """
    try:
        # Очищаем от пробелов
        date_str = date_str.strip()

        # Разделяем по точке
        if "." not in date_str:
            raise ValueError("Нет разделителя '.'")

        day_part, month_part = date_str.split(".")

        # Удаляем пробелы и преобразуем в числа
        day = int(day_part.strip())
        month = int(month_part.strip())

        # Валидация
        if not (1 <= day <= 31):
            raise ValueError("День должен быть 1-31")
        if not (1 <= month <= 12):
            raise ValueError("Месяц должен быть 1-12")

        # Проверка дней в месяце
        days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if day > days_in_month[month - 1]:
            raise ValueError(f"В месяце {month} только {days_in_month[month-1]} дней")

        # Возвращаем с ведущими нулями
        return f"{day:02d}.{month:02d}"

    except ValueError as e:
        raise ValueError(f"Неверный формат даты: {e}")
    except Exception:
        raise ValueError("Используйте формат ДД.ММ (например, 15.01)")


def normalize_time(date_str: str) -> str:
    """
    Принимает время в любом формате (h-m, hh-m, h-mm, hh-mm)
    Возвращает нормализованное время в формате HH-MM
    """
    try:
        # Очищаем от пробелов
        date_str = date_str.strip()

        # Разделяем по тире
        if "-" not in date_str:
            raise ValueError("Нет разделителя '-'")

        hour_part, minut_part = date_str.split("-")

        # Удаляем пробелы и преобразуем в числа
        hour = int(hour_part)
        minut = int(minut_part)

        # Валидация
        if not (0 <= hour <= 23):
            raise ValueError("Час должен быть от 0 до 23")
        if not (0 <= minut <= 59):
            raise ValueError("Минуты должны быть от 0 до 59")

        # Возвращаем с ведущими нулями
        return f"{hour:02d}-{minut:02d}"

    except ValueError as e:
        raise ValueError(f"Неверный формат времени: {e}")
    except Exception:
        raise ValueError("Используйте формат HH-MM (например, 13-25)")


# ОБРАБОТЧИК НАЖАТИЯ НА КНОПКУ "Добавить" (НАЧАЛО ПРОЦЕССА)
@router.callback_query(F.data == "monthly_reminders_write")
async def add_monthly_reminder_start(callback: CallbackQuery, state: FSMContext):
    """
    Эта функция вызывается когда пользователь нажимает на inline-кнопку
    с callback_data="monthly_reminders_write"

    Параметры:
    - callback: CallbackQuery - информация о нажатии кнопки
    - state: FSMContext - объект для управления состоянием пользователя
    """

    # Отправляем пользователю сообщение с просьбой ввести число
    await callback.message.answer("Введите число от 1 до 31:")

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
    2. ТЕКУЩЕЕ состояние пользователя = AddMonthlyReminder.date

    Функция получает число от пользователя, проверяет его корректность
    и переводит к следующему шагу
    """
    try:
        day = int(message.text)
        if day < 1 or day > 31:
            await message.answer(
                "❌ Ошибка: число должно быть от 1 до 31. Пожалуйста, введите корректное число:"
            )
            return
    except ValueError:
        # Если пользователь ввел не число, отправляем сообщение об ошибке
        await message.answer(
            "❌ Ошибка: необходимо ввести число. Пожалуйста, введите число от 1 до 31:"
        )
        return  # Выходим из обработчика, состояние не меняется

    # ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО
    # Сохраняем введенное число во временное хранилище FSM
    # update_data() добавляет или обновляет данные в хранилище состояний
    # Эти данные будут доступны на следующих шагах
    await state.update_data(date=message.text)

    # Меняем состояние пользователя на следующее
    # Теперь будем ждать ввод события
    await state.set_state(AddMonthlyReminder.event)

    # Просим пользователя ввести событие
    await message.answer("Введите ежемесячное событие:")


# ОБРАБОТЧИК ВВОДА СОБЫТИЯ (ВТОРОЙ ШАГ И СОХРАНЕНИЕ В БД)
@router.message(AddMonthlyReminder.event)
async def save_event_monthly_reminders(message: Message, state: FSMContext):
    """
    Эта функция вызывается когда:
    1. Пользователь отправил текстовое сообщение
    2. ТЕКУЩЕЕ состояние пользователя = AddMonthlyReminder.event

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

    if not event:
        await message.answer("Событие не может быть пустым:")
        return

    try:
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
                "CREATE TABLE IF NOT EXISTS monthly_reminders (id INTEGER PRIMARY KEY, date TEXT, event TEXT)"
            )

            # Вставляем данные в таблицу
            # ? - placeholders для защиты от SQL-инъекций
            # (date, event) - кортеж значений, которые подставятся вместо ?
            conn.execute(
                "INSERT INTO monthly_reminders (date, event) VALUES (?, ?)",
                (date, event),
            )
            # commit() вызывается автоматически при выходе из блока with

        # ЗАВЕРШЕНИЕ ПРОЦЕССА
        # Очищаем состояние пользователя
        # clear() удаляет все данные из хранилища FSM для этого пользователя
        # Пользователь возвращается в "нейтральное" состояние
        await state.clear()
        await message.answer(f"Событие {date} {event} успешно добавлено в БД")

    except sqlite3.Error as e:
        # Перехватывает ВСЕ ошибки SQLite
        await message.answer(f"❌ Ошибка базы данных: {str(e)}")
        print(f"Database error: {e}")  # Логгирование

    except Exception as e:
        # Перехватывает все остальные ошибки
        await message.answer("❌ Произошла непредвиденная ошибка")
        print(f"Unexpected error: {e}")  # Логгирование


@router.callback_query(F.data == "monthly_reminders_delete")
async def delete_monthly_reminder_start(callback: CallbackQuery, state: FSMContext):
    """
    Эта функция вызывается когда пользователь нажимает на inline-кнопку
    с callback_data="monthly_reminders_delete"
    """
    # ПРОВЕРКА ПОДКЛЮЧЕНИЯ К БАЗЕ ДАННЫХ
    try:
        # Пробуем подключиться к базе данных
        with sqlite3.connect("db/calendar.db") as conn:
            cursor = conn.cursor()

            # Проверяем, существует ли таблица
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='monthly_reminders'"
            )
            if not cursor.fetchone():
                await callback.message.answer("📭 База данных пуста. Нечего удалять.")
                return

            # Получаем все записи из таблицы
            cursor.execute("SELECT id, date, event FROM monthly_reminders ORDER BY id")
            records = cursor.fetchall()

            if not records:
                await callback.message.answer("📭 База данных пуста. Нечего удалять.")
                return

            # Формируем сообщение со списком записей
            message_text = "📋 Список ежемесячных напоминаний:\n\n"
            for record in records:
                id_num, date, event = record
                message_text += (
                    f"<b>ID - {str(id_num).ljust(4)}</b> {event} - {str(date)} число\n"
                )

            message_text += "\nВведите ID записи, которую хотите удалить:"

        await callback.message.answer(message_text, parse_mode="HTML")

        # Устанавливаем начальное состояние для удаления
        await state.set_state(DeleteMonthlyReminder.select_id)

    except sqlite3.Error as e:
        # Перехватывает ВСЕ ошибки SQLite
        await callback.answer(f"❌ Ошибка базы данных: {str(e)}")
        print(f"Database error: {e}")  # Логгирование

    except Exception as e:
        # Перехватывает все остальные ошибки
        await callback.answer("❌ Произошла непредвиденная ошибка")
        print(f"Unexpected error: {e}")  # Логгирование


@router.message(DeleteMonthlyReminder.select_id)
async def select_id_for_delete_monthly_reminder(message: Message, state: FSMContext):
    """
    Упрощенный вариант: удаляем сразу после ввода ID
    """
    try:
        record_id = int(message.text.strip())

        with sqlite3.connect("db/calendar.db") as conn:
            cursor = conn.cursor()

            # Сначала получаем информацию о записи для отчета
            cursor.execute(
                "SELECT date, event FROM monthly_reminders WHERE id = ?", (record_id,)
            )
            record = cursor.fetchone()

            if not record:
                await message.answer(
                    f"❌ Запись с ID {record_id} не найдена. Введите ID из списка."
                )
                return

            date, event = record

            # Удаляем запись
            cursor.execute("DELETE FROM monthly_reminders WHERE id = ?", (record_id,))

            await message.answer(
                f"✅ Запись успешно удалена:\n"
                f"ID: {record_id}\n"
                f"Число: {date}\n"
                f"Событие: {event}"
            )

    except ValueError:
        await message.answer(
            "❌ Пожалуйста, введите корректный номер ID (целое число):"
        )
        return

    except sqlite3.Error as e:
        # Перехватывает ВСЕ ошибки SQLite
        await message.answer(f"❌ Ошибка базы данных: {str(e)}")
        print(f"Database error: {e}")  # Логгирование

    except Exception as e:
        # Перехватывает все остальные ошибки
        await message.answer("❌ Произошла непредвиденная ошибка")
        print(f"Unexpected error: {e}")  # Логгирование

    # Очищаем состояние
    await state.clear()


@router.callback_query(F.data == "annual_reminders_write")
async def add_annual_reminder_start(callback: CallbackQuery, state: FSMContext):
    """
    Эта функция вызывается когда пользователь нажимает на inline-кнопку
    с callback_data="annual_reminders_write"

    Параметры:
    - callback: CallbackQuery - информация о нажатии кнопки
    - state: FSMContext - объект для управления состоянием пользователя
    """

    # Отправляем пользователю сообщение с просьбой ввести число
    await callback.message.answer("📅 Введите дату (ДД.ММ):")

    # Устанавливаем начальное состояние для этого пользователя
    # set_state() переводит пользователя в указанное состояние
    # Теперь все сообщения от этого пользователя будут проверяться на соответствие этому состоянию
    await state.set_state(AddAnnualReminder.date)


@router.message(AddAnnualReminder.date)
async def save_date_annual_reminders(message: Message, state: FSMContext):
    """
    Эта функция вызывается когда:
    1. Пользователь отправил текстовое сообщение
    2. ТЕКУЩЕЕ состояние пользователя = AddAnnualReminder.date

    Функция получает число от пользователя и переводит его к следующему шагу
    """
    try:
        # Нормализуем дату
        date = normalize_date(message.text)
        # Сохраняем введенное число во временное хранилище FSM
        # update_data() добавляет или обновляет данные в хранилище состояний
        # Эти данные будут доступны на следующих шагах
        await state.update_data(date=date)

        # Меняем состояние пользователя на следующее
        # Теперь будем ждать ввод события
        await state.set_state(AddAnnualReminder.event)

        # Просим пользователя ввести событие
        await message.answer("Введите ежегодное событие:")

    except ValueError as e:
        await message.answer(f"❌ {e}\nПопробуйте еще раз:")


@router.message(AddAnnualReminder.event)
async def save_event_annual_reminders(message: Message, state: FSMContext):
    """
    Эта функция вызывается когда:
    1. Пользователь отправил текстовое сообщение
    2. ТЕКУЩЕЕ состояние пользователя = AddAnnualReminder.event

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

    if not event:
        await message.answer("Событие не может быть пустым:")
        return

    try:
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
                "CREATE TABLE IF NOT EXISTS annual_reminders (id INTEGER PRIMARY KEY, date TEXT, event TEXT)"
            )

            # Вставляем данные в таблицу
            # ? - placeholders для защиты от SQL-инъекций
            # (date, event) - кортеж значений, которые подставятся вместо ?
            conn.execute(
                "INSERT INTO annual_reminders (date, event) VALUES (?, ?)",
                (date, event),
            )
            # commit() вызывается автоматически при выходе из блока with

        # ЗАВЕРШЕНИЕ ПРОЦЕССА
        # Очищаем состояние пользователя
        # clear() удаляет все данные из хранилища FSM для этого пользователя
        # Пользователь возвращается в "нейтральное" состояние
        await state.clear()
        await message.answer(f"Событие {date} {event} успешно добавлено в БД")

    except sqlite3.Error as e:
        # Перехватывает ВСЕ ошибки SQLite
        await message.answer(f"❌ Ошибка базы данных: {str(e)}")
        print(f"Database error: {e}")  # Логгирование

    except Exception as e:
        # Перехватывает все остальные ошибки
        await message.answer("❌ Произошла непредвиденная ошибка")
        print(f"Unexpected error: {e}")  # Логгирование


@router.callback_query(F.data == "annual_reminders_delete")
async def delete_annual_reminder_start(callback: CallbackQuery, state: FSMContext):
    """
    Эта функция вызывается когда пользователь нажимает на inline-кнопку
    с callback_data="annual_reminders_delete"
    """

    try:
        # Сначала покажем пользователю список существующих записей
        with sqlite3.connect("db/calendar.db") as conn:
            cursor = conn.cursor()

            # Проверяем, существует ли таблица
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='annual_reminders'"
            )
            if not cursor.fetchone():
                await callback.message.answer("📭 База данных пуста. Нечего удалять.")
                return

            # Получаем все записи из таблицы
            cursor.execute("SELECT id, date, event FROM annual_reminders ORDER BY id")
            records = cursor.fetchall()

            if not records:
                await callback.message.answer("📭 База данных пуста. Нечего удалять.")
                return

            # Формируем сообщение со списком записей
            message_text = "📋 Список ежегодных напоминаний:\n\n"
            for record in records:
                id_num, date, event = record
                message_text += (
                    f"<b>ID - {str(id_num).ljust(4)}</b>  {event} - {str(date)}\n"
                )

            message_text += "\nВведите ID записи, которую хотите удалить:"

        await callback.message.answer(message_text, parse_mode="HTML")

        # Устанавливаем начальное состояние для удаления
        await state.set_state(DeleteAnnualReminder.select_id)

    except sqlite3.Error as e:
        # Перехватывает ВСЕ ошибки SQLite
        await callback.answer(f"❌ Ошибка базы данных: {str(e)}")
        print(f"Database error: {e}")  # Логгирование

    except Exception as e:
        # Перехватывает все остальные ошибки
        await callback.answer("❌ Произошла непредвиденная ошибка")
        print(f"Unexpected error: {e}")  # Логгирование


@router.message(DeleteAnnualReminder.select_id)
async def select_id_for_delete_annual_reminder(message: Message, state: FSMContext):
    """
    Упрощенный вариант: удаляем сразу после ввода ID
    """
    try:
        record_id = int(message.text.strip())

        with sqlite3.connect("db/calendar.db") as conn:
            cursor = conn.cursor()

            # Сначала получаем информацию о записи для отчета
            cursor.execute(
                "SELECT date, event FROM annual_reminders WHERE id = ?", (record_id,)
            )
            record = cursor.fetchone()

            if not record:
                await message.answer(
                    f"❌ Запись с ID {record_id} не найдена. Введите ID из списка."
                )
                return

            date, event = record

            # Удаляем запись
            cursor.execute("DELETE FROM annual_reminders WHERE id = ?", (record_id,))

            await message.answer(
                f"✅ Запись успешно удалена:\n"
                f"ID: {record_id}\n"
                f"Дата: {date}\n"
                f"Событие: {event}"
            )

    except ValueError:
        await message.answer(
            "❌ Пожалуйста, введите корректный номер ID (целое число):"
        )
        return

    except sqlite3.Error as e:
        # Перехватывает ВСЕ ошибки SQLite
        await message.answer(f"❌ Ошибка базы данных: {str(e)}")
        print(f"Database error: {e}")  # Логгирование

    except Exception as e:
        # Перехватывает все остальные ошибки
        await message.answer("❌ Произошла непредвиденная ошибка")
        print(f"Unexpected error: {e}")  # Логгирование

    # Очищаем состояние
    await state.clear()


@router.callback_query(F.data == "onetime_reminders_write")
async def add_onetime_reminder_start(callback: CallbackQuery, state: FSMContext):
    """
    Эта функция вызывается когда пользователь нажимает на inline-кнопку
    с callback_data="onetime_reminders_write"

    Параметры:
    - callback: CallbackQuery - информация о нажатии кнопки
    - state: FSMContext - объект для управления состоянием пользователя
    """

    # Отправляем пользователю сообщение с просьбой ввести число
    await callback.message.answer("📅 Введите дату (ДД.ММ):")

    # Устанавливаем начальное состояние для этого пользователя
    # set_state() переводит пользователя в указанное состояние
    # Теперь все сообщения от этого пользователя будут проверяться на соответствие этому состоянию
    await state.set_state(AddOnetimeReminder.date)


@router.message(AddOnetimeReminder.date)
async def save_date_onetime_reminders(message: Message, state: FSMContext):
    """
    Эта функция вызывается когда:
    1. Пользователь отправил текстовое сообщение
    2. ТЕКУЩЕЕ состояние пользователя = AddOnetimeReminder.date

    Функция получает число от пользователя и переводит его к следующему шагу
    """
    try:
        # Нормализуем дату
        date = normalize_date(message.text)
        # Сохраняем введенное число во временное хранилище FSM
        # update_data() добавляет или обновляет данные в хранилище состояний
        # Эти данные будут доступны на следующих шагах
        await state.update_data(date=date)

        # Меняем состояние пользователя на следующее
        # Теперь будем ждать ввод события
        await state.set_state(AddOnetimeReminder.time)

        # Просим пользователя ввести событие
        await message.answer("⌚ Введите время в формате (HH-MM):")

    except ValueError as e:
        await message.answer(f"❌ {e}\nПопробуйте еще раз:")


@router.message(AddOnetimeReminder.time)
async def save_time_onetime_reminders(message: Message, state: FSMContext):
    """
    Эта функция вызывается когда:
    1. Пользователь отправил текстовое сообщение
    2. ТЕКУЩЕЕ состояние пользователя = AddOnetimeReminder.time

    Функция получает число от пользователя и переводит его к следующему шагу
    """
    try:
        # Нормализуем дату
        time = normalize_time(message.text)
        # Сохраняем введенное число во временное хранилище FSM
        # update_data() добавляет или обновляет данные в хранилище состояний
        # Эти данные будут доступны на следующих шагах
        await state.update_data(time=time)

        # Меняем состояние пользователя на следующее
        # Теперь будем ждать ввод события
        await state.set_state(AddOnetimeReminder.event)

        # Просим пользователя ввести событие
        await message.answer("Введите одноразовое событие:")

    except ValueError as e:
        await message.answer(f"❌ {e}\nПопробуйте еще раз:")


@router.message(AddOnetimeReminder.event)
async def save_event_onetime_reminders(message: Message, state: FSMContext):
    """
    Эта функция вызывается когда:
    1. Пользователь отправил текстовое сообщение
    2. ТЕКУЩЕЕ состояние пользователя = AddOnetimeReminder.event

    Функция получает событие и сохраняет все данные в базу данных
    """
    data = await state.get_data()

    date = data["date"]
    time = data["time"]
    event = message.text

    if not event:
        await message.answer("Событие не может быть пустым:")
        return

    try:
        with sqlite3.connect("db/calendar.db") as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS onetime_reminders (id INTEGER PRIMARY KEY, date TEXT, time TEXT, event TEXT)"
            )
            conn.execute(
                "INSERT INTO onetime_reminders (date, time, event) VALUES (?, ?, ?)",
                (date, time, event),
            )

        await state.clear()
        await message.answer(f"Событие {date} {time} {event} успешно добавлено в БД")

    except sqlite3.Error as e:
        await message.answer(f"❌ Ошибка базы данных: {str(e)}")
        print(f"Database error: {e}")  # Логгирование

    except Exception as e:
        await message.answer("❌ Произошла непредвиденная ошибка")
        print(f"Unexpected error: {e}")  # Логгирование


@router.callback_query(F.data == "onetime_reminders_delete")
async def delete_onetime_reminder_start(callback: CallbackQuery, state: FSMContext):
    """
    Эта функция вызывается когда пользователь нажимает на inline-кнопку
    с callback_data="onetime_reminders_delete"
    """

    try:
        # Сначала покажем пользователю список существующих записей
        with sqlite3.connect("db/calendar.db") as conn:
            cursor = conn.cursor()

            # Проверяем, существует ли таблица
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='onetime_reminders'"
            )
            if not cursor.fetchone():
                await callback.message.answer("📭 Такой таблицы нет в БД.")
                return

            # Получаем все записи из таблицы
            cursor.execute(
                "SELECT id, date, time, event FROM onetime_reminders ORDER BY id"
            )
            records = cursor.fetchall()

            if not records:
                await callback.message.answer("📭 База данных пуста. Нечего удалять.")
                return

            # Формируем сообщение со списком записей
            message_text = "📋 Список одноразовых напоминаний:\n\n"
            for record in records:
                id_num, date, time, event = record
                message_text += (
                    f"<b>ID - {str(id_num).ljust(4)}</b>  {event} - {date} {time}\n"
                )

            message_text += "\nВведите ID записи, которую хотите удалить:"

        await callback.message.answer(message_text, parse_mode="HTML")

        # Устанавливаем начальное состояние для удаления
        await state.set_state(DeleteOnetimeReminder.select_id)

    except sqlite3.Error as e:
        # Перехватывает ВСЕ ошибки SQLite
        await callback.answer(f"❌ Ошибка базы данных: {str(e)}")
        print(f"Database error: {e}")  # Логгирование

    except Exception as e:
        # Перехватывает все остальные ошибки
        await callback.answer("❌ Произошла непредвиденная ошибка")
        print(f"Unexpected error: {e}")  # Логгирование


@router.message(DeleteOnetimeReminder.select_id)
async def select_id_for_delete_onetime_reminder(message: Message, state: FSMContext):
    """
    Упрощенный вариант: удаляем сразу после ввода ID
    """
    try:
        record_id = int(message.text.strip())

        with sqlite3.connect("db/calendar.db") as conn:
            cursor = conn.cursor()

            # Сначала получаем информацию о записи для отчета
            cursor.execute(
                "SELECT date, time, event FROM onetime_reminders WHERE id = ?",
                (record_id,),
            )
            record = cursor.fetchone()

            if not record:
                await message.answer(
                    f"❌ Запись с ID {record_id} не найдена. Введите ID из списка."
                )
                return

            date, time, event = record

            # Удаляем запись
            cursor.execute("DELETE FROM onetime_reminders WHERE id = ?", (record_id,))

            await message.answer(
                f"✅ Запись успешно удалена:\n"
                f"ID: {record_id}\n"
                f"Дата: {date}\n"
                f"Время: {time}\n"
                f"Событие: {event}"
            )

    except ValueError:
        await message.answer(
            "❌ Пожалуйста, введите корректный номер ID (целое число):"
        )
        return

    except sqlite3.Error as e:
        # Перехватывает ВСЕ ошибки SQLite
        await message.answer(f"❌ Ошибка базы данных: {str(e)}")
        print(f"Database error: {e}")  # Логгирование

    except Exception as e:
        # Перехватывает все остальные ошибки
        await message.answer("❌ Произошла непредвиденная ошибка")
        print(f"Unexpected error: {e}")  # Логгирование

    # Очищаем состояние
    await state.clear()
