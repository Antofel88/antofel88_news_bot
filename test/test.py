from aiogram import Bot
import sqlite3

import requests
from bs4 import BeautifulSoup

import time
from datetime import date
from datetime import datetime, timedelta

import random
import re


def fix_to_dd_mm_format_debug():
    """
    Преобразует даты из ММ-ДД в ДД.ММ с подробным выводом
    """
    import sqlite3

    print("🔍 НАЧАЛО ДИАГНОСТИКИ")
    print("=" * 50)

    with sqlite3.connect("db/calendar.db") as conn:
        cursor = conn.cursor()

        # 1. Проверяем структуру таблицы
        cursor.execute("PRAGMA table_info(annual_reminders)")
        columns = cursor.fetchall()
        print("📋 Структура таблицы:")
        for col in columns:
            print(f"   {col[1]} ({col[2]})")

        # 2. Считаем общее количество записей
        cursor.execute("SELECT COUNT(*) FROM annual_reminders")
        total = cursor.fetchone()[0]
        print(f"\n📊 Всего записей в таблице: {total}")

        # 3. Показываем первые 5 записей "как есть"
        cursor.execute("SELECT id, date FROM annual_reminders LIMIT 5")
        samples = cursor.fetchall()
        print("\n📝 Примеры записей (первые 5):")
        for id_num, date in samples:
            print(f"   ID {id_num}: '{date}' (длина: {len(date)})")

        # 4. Анализируем форматы дат
        cursor.execute("SELECT id, date FROM annual_reminders")
        all_records = cursor.fetchall()

        formats_count = {
            "with_hyphen": 0,  # ММ-ДД
            "with_dot": 0,  # ДД.ММ или Д.М
            "other": 0,
        }

        print("\n🔎 Анализ форматов:")
        for id_num, date in all_records:
            if "-" in date:
                formats_count["with_hyphen"] += 1
            elif "." in date:
                formats_count["with_dot"] += 1
            else:
                formats_count["other"] += 1

        print(f"   С дефисом (-): {formats_count['with_hyphen']}")
        print(f"   С точкой (.): {formats_count['with_dot']}")
        print(f"   Другой формат: {formats_count['other']}")

        # 5. Если есть записи с дефисом - конвертируем их
        if formats_count["with_hyphen"] > 0:
            print("\n🔄 КОНВЕРТАЦИЯ ЗАПИСЕЙ С ДЕФИСОМ:")

            cursor.execute(
                "SELECT id, date FROM annual_reminders WHERE date LIKE '%-%'"
            )
            records_to_fix = cursor.fetchall()

            fixed_count = 0
            for id_num, old_date in records_to_fix:
                try:
                    # Разделяем по дефису
                    month, day = old_date.split("-")

                    # Очищаем от пробелов
                    month = month.strip()
                    day = day.strip()

                    # Добавляем ведущие нули
                    month = month.zfill(2)
                    day = day.zfill(2)

                    # Новый формат: ДД.ММ
                    new_date = f"{day}.{month}"

                    # Обновляем запись
                    cursor.execute(
                        "UPDATE annual_reminders SET date = ? WHERE id = ?",
                        (new_date, id_num),
                    )

                    print(f"   ✅ ID {id_num}: '{old_date}' -> '{new_date}'")
                    fixed_count += 1

                except Exception as e:
                    print(f"   ❌ Ошибка с ID {id_num}: {e}")

            conn.commit()
            print(f"\n✅ Сконвертировано {fixed_count} записей")

        # 6. Принудительно обновляем ВСЕ записи до формата ДД.ММ
        print("\n🔄 ПРОВЕРКА ВСЕХ ЗАПИСЕЙ:")

        cursor.execute("SELECT id, date FROM annual_reminders")
        all_records = cursor.fetchall()

        normalized_count = 0
        for id_num, old_date in all_records:
            try:
                # Очищаем от пробелов
                old_date = old_date.strip()

                # Определяем разделитель
                if "-" in old_date:
                    month, day = old_date.split("-")
                elif "." in old_date:
                    day, month = old_date.split(".")
                else:
                    print(f"   ⚠️ ID {id_num}: непонятный формат '{old_date}'")
                    continue

                # Очищаем от пробелов
                day = day.strip()
                month = month.strip()

                # Добавляем ведущие нули
                day = day.zfill(2)
                month = month.zfill(2)

                # Формируем правильную дату
                new_date = f"{day}.{month}"

                # Если дата изменилась - обновляем
                if new_date != old_date:
                    cursor.execute(
                        "UPDATE annual_reminders SET date = ? WHERE id = ?",
                        (new_date, id_num),
                    )
                    print(f"   🔄 ID {id_num}: '{old_date}' -> '{new_date}'")
                    normalized_count += 1
                else:
                    print(f"   ✅ ID {id_num}: уже в правильном формате '{old_date}'")

            except Exception as e:
                print(f"   ❌ Ошибка с ID {id_num}: {e}")

        conn.commit()

        # 7. Финальная проверка
        print("\n📊 РЕЗУЛЬТАТ:")
        cursor.execute("SELECT id, date FROM annual_reminders ORDER BY id")
        final_records = cursor.fetchall()

        all_good = True
        for id_num, date in final_records:
            if len(date) == 5 and date[2] == ".":
                status = "✅"
            else:
                status = "❌"
                all_good = False
            print(f"   {status} ID {id_num}: '{date}'")

        print("=" * 50)
        if all_good:
            print("🎉 ВСЕ ДАТЫ В ПРАВИЛЬНОМ ФОРМАТЕ ДД.ММ!")
        else:
            print("⚠️ ЕСТЬ ПРОБЛЕМНЫЕ ЗАПИСИ!")

        print(f"📈 Нормализовано записей: {normalized_count}")


# ЗАПУСК
if __name__ == "__main__":
    fix_to_dd_mm_format_debug()
