import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage


logger = logging.getLogger(__name__)

token = os.environ.get('BOT_TOKEN', False) 
if token:
    # инициализация бота и диспетчера
    bot = Bot(token=token, parse_mode='HTML')
    dp = Dispatcher(bot,storage=MemoryStorage())
else:
    logging.error('Не указана переменная окружения BOT_TOKEN! Выход')
    exit(1)
