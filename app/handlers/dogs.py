from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.orm import session, User, Dog
from app import logger

from app import dp


class Registration(StatesGroup):
    '''Класс ожидания состояний регистрации'''
    waiting_for_dog_name = State()
    waiting_for_dog_confirm = State()


async def dog_registration(message: types.Message, state: FSMContext):
    '''
        1. Спросить про кличку собаки
    '''
    await message.answer("Как зовут вашу собаку?", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Registration.waiting_for_dog_name.state)


async def dog_registration_entered(message: types.Message, state: FSMContext):
    '''
        2. занести введеный текст, как кличку собаки в память состояния
    '''
    if message.text == 'Нет, изменить кличку':
        await message.answer('Тогда введите другое имя', reply_markup=types.ReplyKeyboardRemove())
    

    if message.text == 'Сохранить':
        dog = await state.get_data()
        logger.debug(dog)
        user_meta = message.chat.values
        our_user = session.query(User).filter_by(t_chat_id=user_meta['id']).first()
        new_dog = Dog(dog['dog_name'], our_user.id)
        session.add(new_dog)
        session.commit()
        await message.answer("Сохранено", reply_markup=types.ReplyKeyboardRemove())
        state.finish()
        return

    await state.update_data(dog_name=message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Сохранить")
    keyboard.add("Нет, изменить кличку")
    keyboard.add("Отмена")
    await message.answer(f"Сохранить собаку под кличкой: {message.text}?", reply_markup=keyboard)
    # await state.set_state(Registration.waiting_for_dog_confirm.state)



# -------------------------------- МОИ СОБАКИ -------------------------------- #
async def my_dogs(message: types.Message):
    # Прочитать данные чата и найти юзера в БД
    user_meta = message.chat.values
    our_user = session.query(User).filter_by(t_chat_id=user_meta['id']).first()
    await message.answer(
        f"Количество собак: {our_user.dogs.count()}.\n{{*our_user.dogs}}"
    )

def register_handlers_dog_names(dp: Dispatcher):
    '''
        Зарегистрировать функции создания собаки
    '''
    dp.register_message_handler(dog_registration, commands="newdog", state="*")
    dp.register_message_handler(dog_registration_entered, state=Registration.waiting_for_dog_name)
    



