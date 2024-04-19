from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from app.orm import session, User




async def cmd_start(message: types.Message, state: FSMContext):
    # Завершить состояние предыдущего диалога
    await state.finish()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    buttons = ["ℹ️ Информация"]
    
    # Прочитать данные чата и найти юзера в БД
    user_meta = message.chat.values
    our_user = session.query(User).filter_by(t_chat_id=user_meta['id']).first()
    
    if our_user:
        buttons.append("💬 Профиль")
        buttons.append("🐾 Играть")
    else:
        buttons.append("📝 Регистрация")
    
    # Добавить кнопки
    keyboard.add(*buttons)

    await message.answer(
        f"Привет) {message.chat.values['first_name']} ✌️ Я Терра-бот 🐺\nЕсли вы меня не знаете, то пожалуйста, не пишите мне.\nНажми на нужную кнопку меню, чтобы начать работу ✍",
        reply_markup=keyboard
    )
# -------------------------------- Профиль -------------------------------- #
async def profile(message: types.Message):
    # Прочитать данные чата и найти юзера в БД
    user_meta = message.chat.values
    our_user = session.query(User).filter_by(t_chat_id=user_meta['id']).first()
    
    await message.reply(f'''Вот ваш профиль:\n{our_user}\n----
    ''')
# ---------------------------------------------------------------------------- #
# -------------------------------- Информация -------------------------------- #

async def information(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply(f'Это заглушка для информации по проекту. Ща ничего тут нет(')
# ---------------------------------------------------------------------------- #
# -------------------------------- Регистрация ------------------------------- #

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
# ---------------------------------------------------------------------------- #

async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено\nНапиши /start, для входа в меню, или выбери опции из списка команд ", reply_markup=types.ReplyKeyboardRemove())

def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(profile, Text(equals="💬 Профиль", ignore_case=True), state="*")
    dp.register_message_handler(profile, commands="profile", state="*")
    dp.register_message_handler(information, Text(equals="ℹ️ Информация", ignore_case=True), state="*")
    dp.register_message_handler(cmd_registration, Text(equals="📝 Регистрация", ignore_case=True), state="*")