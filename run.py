import logging
import os
from aiogram import Bot, Dispatcher, executor, types

from orm import session, User

# Configure logging
logging.basicConfig(level=logging.INFO)

token = os.environ.get('BOT_TOKEN', False) 
if token:
    # инициализация бота и диспетчера
    bot = Bot(token=token, parse_mode='HTML')
    dp = Dispatcher(bot)
else:
    logging.error('Не указана переменная окружения BOT_TOKEN! Выход')
    exit(1)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    logging.info(message.chat.values)

    await message.reply(f"Привет) {message.chat.values['first_name']} ✌️ Я Терра-бот 🐺\nЕсли вы меня не знаете, то пожалуйста, не пишите мне.\nНажми на нужную кнопку меню, чтобы начать работу ✍")

@dp.message_handler(commands=['dice'])
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji='🎲')

@dp.message_handler(commands=['registration'])
async def cmd_registration(message: types.Message):
    user_meta = message.chat.values
    our_user = session.query(User).filter_by(t_chat_id=user_meta['id']).first()
    if our_user:
        await message.reply(f'Я тебя уже знаю) Ты {user_meta["first_name"]} {user_meta["last_name"]}')
    else:
        new_user = User(
            user_meta['id'],
            user_meta['username'],
            user_meta['first_name'],
            user_meta['last_name'],
        )
        session.add(new_user)
        session.commit()
        await message.reply(f'Ок, считай тебя зарегала, ты с нами!')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)