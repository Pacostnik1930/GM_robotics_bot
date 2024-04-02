from telebot import types
import telebot

bot = telebot.TeleBot('7138089393:AAEoBSwwCzVYOaUDEQdv6Vv0ILiaR-LwZ5k')

user_data = {}

def handle_modeling(message, bot):
    chat_id = message.chat.id
    user_data[chat_id] = {'photos': []}
    send_photo_request_modeling(message, bot)

def send_photo_request_modeling(message, bot):
    bot.send_message(message.chat.id, "Пожалуйста, загрузите фото для 3D моделирования.")
    bot.register_next_step_handler(message, handle_photo_modeling, bot)

def handle_photo_modeling(message, bot):
    chat_id = message.chat.id
    if message.photo:
        photo = message.photo[-1].file_id
        if 'photos' not in user_data[chat_id]:
            user_data[chat_id]['photos'] = []  # Инициализируем список фото, если он не существует
        user_data[chat_id]['photos'].append(photo)  # Добавляем загруженное фото в список
        send_buttons_after_photo_modeling(message, bot)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, загрузите фото по одному.")
        bot.register_next_step_handler(message, handle_photo_modeling, bot)

def send_buttons_after_photo_modeling(message, bot):
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Назад', callback_data='back_to_photo_modeling')
    keyboard.row(btn1)
    btn2 = types.InlineKeyboardButton(text='Далее', callback_data='next_step_modeling')
    keyboard.row(btn2)
    btn3 = types.InlineKeyboardButton(text='Добавить еще фото', callback_data='add_photo_modeling')
    keyboard.row(btn3)
    bot.send_message(message.chat.id, "Фото получено. Выберите действие:", reply_markup=keyboard)

def handle_back_to_photo_modeling(call, bot):
    message = call.message
    chat_id = message.chat.id
    if user_data[chat_id]['photos']:
        user_data[chat_id]['photos'].pop()  # Удаляем последнее загруженное фото
    send_photo_request_modeling(message, bot)

def handle_add_photo_modeling(call, bot):
    message = call.message
    send_photo_request_modeling(message, bot)

def handle_next_step_modeling(call, bot):
    message = call.message
    bot.send_message(message.chat.id, "Пожалуйста, опишите требования к 3D модели.")
    bot.register_next_step_handler(message, handle_description_modeling, bot)

def handle_description_modeling(message, bot):
    chat_id = message.chat.id
    description = message.text
    user_data[chat_id]['description'] = description
    bot.send_message(chat_id, "Вы ввели следующие требования к 3D модели:")
    bot.send_message(chat_id, description)
    send_confirmation_buttons_modeling(message, bot)

def send_confirmation_buttons_modeling(message, bot):
    keyboard = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton(text='Подтвердить отправку', callback_data='confirm_send_modeling')
    keyboard.add(btn2)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'confirm_send_modeling')
def handle_confirm_send_modeling(call):
    message = call.message
    chat_id = message.chat.id
    photos = user_data[chat_id]['photos']
    description = user_data[chat_id]['description']
    send_confirmation_modeling(message, bot, photos, description)

def send_confirmation_modeling(message, bot, photos, description):
    bot.send_message(message.chat.id, "Данные отправлены:")
    for photo in photos:
        bot.send_photo(message.chat.id, photo)
    bot.send_message(message.chat.id, f"Требования к 3D модели: {description}")
    bot.send_message(message.chat.id, "С вами свяжутся в ближайшее время. Чтобы создать новое обращение, нажмите /start.")
    del user_data[message.chat.id]