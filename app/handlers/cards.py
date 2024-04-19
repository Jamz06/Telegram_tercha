from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text


from app.orm import session, User, Dog, Sport, Card, CardType
from app import logger


class TaskStates(StatesGroup):
    '''Ожидание состояний в вопросах по задачам'''
    waiting_for_sport = State()
    waiting_for_card_type = State()
    waiting_for_card = State()

async def new_task(message: types.Message, state: FSMContext):
    '''
        Взять новую карточку
    '''
    # 1. Выбрать вид спорта
    # 2. Выбрать тип карточки
    # 3. Выбрать карточку
    # 4. Предложить сразу решить

    sports = session.query(Sport).all()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Отмена"]
    for sport in sports:
        buttons.append(sport.__repr__())
    

    keyboard.add(*buttons)

    await message.answer("Выбери вид спорта", reply_markup=keyboard)
    await state.set_state(TaskStates.waiting_for_sport.state)


async def card_type_select(message: types.Message, state: FSMContext):
    '''
        Выбрать тип карточки в спорте
    '''
    sport = session.query(Sport).filter_by(name=message.text)

    if not sport.first():
        await message.answer("Выбери спорт, используя клавиатуру ниже")
        return

    await state.update_data(chosen_sport=sport[0].id)

    # Типы карточек
    sport = session.query(Sport).filter_by(name=message.text).first()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Отмена"]

    # Развернуть результат запроса видов карточек в список
    buttons.extend([r.__repr__() for r in sport.card_types])
    

    keyboard.add(*buttons)
    
    await state.set_state(TaskStates.waiting_for_card_type.state)
    await message.answer("Выбери вид карточки", reply_markup=keyboard)
    
async def card_select(message: types.Message, state: FSMContext):
    '''
        Выбрать карточку
    '''

    card_type = session.query(CardType).filter_by(name=message.text)
    # Карточки
    if not card_type.first():
        await message.answer("Выбери тип карточки, используя клавиатуру ниже")
        return
    
    # Занести выбранный вид карточки в state
    await state.update_data(chosen_card_type=card_type[0].card_type)
    
    # Показать клавиатуру с карточками
    cards = session.query(Card).filter_by(card_type=card_type[0].card_type)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Отмена"]
    buttons.extend([r.__repr__() for r in cards])

    keyboard.add(*buttons)
    
    await state.set_state(TaskStates.waiting_for_card.state)
    await message.answer("Выбери карточку", reply_markup=keyboard)



def register_handlers_cards(dp: Dispatcher):
    '''
        Зарегистрировать функции работы с карточками
    '''
    dp.register_message_handler(new_task, commands="go", state="*")
    dp.register_message_handler(new_task, Text(equals="🐾 Играть", ignore_case=True), state="*")
    dp.register_message_handler(card_type_select, state=TaskStates.waiting_for_sport)
    dp.register_message_handler(card_select, state=TaskStates.waiting_for_card_type)
    
