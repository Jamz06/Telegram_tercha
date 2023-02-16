import telebot
from telebot import types

import config

#  инициализация бота
bot = telebot.TeleBot(config.BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    # Метод создания кнопок в чате при команде start
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Описание кнопок
    btn_hello = types.InlineKeyboardButton(text='👋 Информация')
    btn1 = types.InlineKeyboardButton(text='💬 Посмотреть мой статус')
    btn2 = types.InlineKeyboardButton(text='📷 Отправить фото')
    # Добавить в ответ
    markup.add(btn_hello,btn1,btn2)
    # ответ бота
    bot.send_message(message.chat.id, "Привет)✌️ Я Терра-бот 🐺, если вы меня не знаете, то пожалуйста, не пишите мне. Нажми на нужную кнопку меню, чтобы начать работу ✍", reply_markup=markup)
    

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == '👋 Информация':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('🎮Правила игры')
        btn2 = types.KeyboardButton('🤳 Контактная информация')
        btn3 = types.KeyboardButton('🧠 Советы')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, '❓ Задайте интересующий вопрос', reply_markup=markup) #ответ бота

    elif message.text == 'Правила игры':
        bot.send_message(message.chat.id, 'Правила игра таковы и больше не каковы')

    elif message.text == 'Контактная информация':
        bot.send_message(message.chat.id, 'Можешь писать моей хозяйке @Kassandra_Aleks')

    elif message.text == 'Отправить фото':
        bot.send_message(message.chat.id, 'Пока фотку не отправить, но можешь кинуть 📷')


# запуск
bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть