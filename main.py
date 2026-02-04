import asyncio
import logging
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import commands_handlers, other_handlers
from handlers.callback_handlers import (
    f1_callback_handlers,
    other_callback_handlers,
    reminders_callback_handlers,
    traktor_callback_handlers,
    ufc_callback_handlers,
)
from states import states

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from alerts.alerts import (
    traktor_next_game_alert,
    ufc_next_tournament_alert,
    f1_next_race_alert,
    monthly_reminders_alert,
    annual_reminders_alert,
)
from update.update_db import (
    traktor_update_db,
    f1_update_db,
)

# Инициализируем логгер
logger = logging.getLogger(__name__)


async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    # Выводим в консоль информацию о начале запуска бота
    logger.info("Starting bot")

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    # Создаем объект scheduler
    scheduler = AsyncIOScheduler(timezone="Asia/Yekaterinburg")
    # Добавляем задания на оповещения
    scheduler.add_job(
        traktor_next_game_alert, trigger="cron", hour=8, kwargs={"bot": bot}
    )

    scheduler.add_job(
        ufc_next_tournament_alert,
        trigger="cron",
        day_of_week="5",
        hour=20,
        kwargs={"bot": bot},
    )
    scheduler.add_job(
        f1_next_race_alert,
        trigger="cron",
        hour=17,
        kwargs={"bot": bot},
    )

    scheduler.add_job(
        monthly_reminders_alert, trigger="cron", hour=8, kwargs={"bot": bot}
    )

    scheduler.add_job(
        annual_reminders_alert, trigger="cron", hour=7, kwargs={"bot": bot}
    )

    # Добавляем задания на обновления баз
    scheduler.add_job(traktor_update_db, trigger="cron", hour=2)
    scheduler.add_job(f1_update_db, trigger="cron", day_of_week=4, hour=16)

    # Запустить выполнение заданий
    scheduler.start()

    # Регистриуем роутеры в диспетчере
    dp.include_router(commands_handlers.router)
    dp.include_router(other_handlers.router)
    dp.include_router(other_callback_handlers.router)
    dp.include_router(traktor_callback_handlers.router)
    dp.include_router(ufc_callback_handlers.router)
    dp.include_router(f1_callback_handlers.router)
    dp.include_router(reminders_callback_handlers.router)
    dp.include_router(states.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
