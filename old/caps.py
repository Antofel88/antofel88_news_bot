# async def washington_next_game_alert(bot: Bot):

#     today = datetime.now()
#     tomorrow = (today + timedelta(days=1)).strftime("%Y-%m-%d")

#     with sqlite3.connect("db/calendar.db") as con:
#         cur = con.cursor()
#         cur.execute(
#             "SELECT date, team, home_guest FROM caps_calendar WHERE date LIKE ?",
#             (f"{tomorrow}%",),
#         )

#         result = cur.fetchall()[0]  # т.к. кортеж в списке

#     if result:
#         event_date, team, home_guest = result

#         if home_guest == "дома":
#             text = f"Завтра {event_date} Вашингтон - {team}\n\nТрансляция VK: https://vkvideo.ru/@36hockey/all"
#         else:
#             text = f"Завтра {event_date} {team} - Вашингтон\n\nТрансляция VK: https://vkvideo.ru/@36hockey/all"

#         await bot.send_message(
#             chat_id="951807751",
#             text=text,
#         )


# async def edmonton_next_game_alert(bot: Bot):

#     today = datetime.now()
#     tomorrow = (today + timedelta(days=1)).strftime("%Y-%m-%d")

#     with sqlite3.connect("db/calendar.db") as con:
#         cur = con.cursor()
#         cur.execute(
#             "SELECT date, team, home_guest FROM edmonton_calendar WHERE date LIKE ?",
#             (f"{tomorrow}%",),
#         )

#         result = cur.fetchall()[0]  # т.к. кортеж в списке

#     if result:
#         event_date, team, home_guest = result

#         if home_guest == "дома":
#             text = f"Завтра {event_date} Эдмонтон - {team}\n\nТрансляция VK: https://vkvideo.ru/@36hockey/all"
#         else:
#             text = f"Завтра {event_date} {team} - Эдмонтон\n\nТрансляция VK: https://vkvideo.ru/@36hockey/all"

#         await bot.send_message(
#             chat_id="951807751",
#             text=text,
#         )

# # Вашингтон
# @router.callback_query(F.data == "washington")
# async def process_washington(callback: CallbackQuery):
#     await callback.message.edit_text(
#         text="🏒 Вашингтон",
#         reply_markup=washington_kb_builder.as_markup(),
#     )


# @router.callback_query(F.data == "washington_next_game")
# async def process_washington_upcoming_game(callback: CallbackQuery):

#     # Создаем объект сегодняшней даты и переводим его в строку
#     current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
#     # Подключение к базе данных (или создание, если её нет)
#     with sqlite3.connect("db/calendar.db") as con:
#         cursor = con.cursor()
#         # Запрос для поиска ближайшего события
#         cursor.execute(
#             """
#         SELECT date, team, home_guest
#         FROM caps_calendar 
#         WHERE date >= ?
#         ORDER BY date
#         LIMIT 1
#         """,
#             (current_date,),
#         )

#         # Получение результата
#         result = cursor.fetchone()

#     if result:
#         event_date, team, home_guest = result

#         if home_guest == "дома":
#             text = f"{event_date} Вашингтон - {team}"
#         else:
#             text = f"{event_date} {team} - Вашингтон"

#         await callback.message.edit_text(
#             text=text,
#             reply_markup=washington_kb_builder.as_markup(),
#         )
#     else:
#         await callback.message.edit_text(
#             text="Ближайших игр не найдено.",
#             reply_markup=washington_kb_builder.as_markup(),
#         )


# @router.callback_query(F.data == "nhl_table")
# async def process_nhl_table(callback: CallbackQuery):
#     url = "https://www.sports.ru/hockey/tournament/nhl/table/"
#     response = requests.get(url=url, headers=headers)
#     soup = BeautifulSoup(response.text, "lxml")

#     west_table_body = soup.find_all({"class": "stat-table", "tbody": ""})
#     west_teams = west_table_body[0].find_all("tr")
#     east_table_body = soup.find_all({"class": "stat-table", "tbody": ""})
#     east_teams = east_table_body[1].find_all("tr")

#     text = "Восточная конференция:\n\n"
#     text += f"                    {"М".ljust(3)} {"О".ljust(3)}\n"
#     for item in west_teams:
#         text += f"{item.text.split("\n")[1].ljust(2)}{item.text.split("\n")[2].ljust(17)}{item.text.split("\n")[3].ljust(3)} {item.text.split("\n")[8].ljust(3)}\n"

#     text += "\nЗападная конференция:\n\n"
#     text += f"                    {"М".ljust(3)} {"О".ljust(3)}\n"

#     for item in east_teams:
#         text += f"{item.text.split("\n")[1].ljust(2)}{item.text.split("\n")[2].ljust(17)}{item.text.split("\n")[3].ljust(3)} {item.text.split("\n")[8].ljust(3)}\n"

#     if callback.message.text != text:
#         await callback.message.edit_text(
#             text=f"`{text}`",
#             reply_markup=washington_kb_builder.as_markup(),
#             parse_mode="MarkdownV2",
#         )
#     else:
#         await callback.answer()
