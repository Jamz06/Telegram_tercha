

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from app.handlers.dogs import register_handlers_dog_names
from app.handlers.common import register_handlers_common
from app.handlers.cards import register_handlers_cards

logger = logging.getLogger(__name__)

# Регистрация команд, отображаемых в интерфейсе Telegram
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать!"),
        BotCommand(command="/cancel", description="Отменить текущее действие"),
        BotCommand(command="/profile", description="Мой профиль"),
        BotCommand(command="/newdog", description="Зарегистрировать собаку"),
        BotCommand(command="/tasks", description="Мои задания"),
        BotCommand(command="/dogs", description="Мои собаки"),
        BotCommand(command="/go", description="Взять карточку")
    ]
    await bot.set_my_commands(commands)


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    # Парсинг файла конфигурации
    
    token = os.environ.get('BOT_TOKEN', False) 
    if token:
        # инициализация бота и диспетчера
        bot = Bot(token=token, parse_mode='HTML')
        dp = Dispatcher(bot,storage=MemoryStorage())
    else:
        logging.error('Не указана переменная окружения BOT_TOKEN! Выход')
        exit(1)


    # Регистрация хэндлеров
    register_handlers_common(dp)
    register_handlers_dog_names(dp)
    register_handlers_cards(dp)
    
    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())