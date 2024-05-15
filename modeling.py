import json
from telebot import types
import telebot
import sqlite3
import _globals
import mysql.connector

bot = telebot.TeleBot('7138089393:AAEoBSwwCzVYOaUDEQdv6Vv0ILiaR-LwZ5k')

user_data = {}

def handle_modeling(message, bot):
    user_data[_globals.gchat_id] = {'photos': []}
    send_photo_request_modeling(message, bot)

def send_photo_request_modeling(message, bot):
    bot.send_message(message.chat.id, "Пожалуйста, загрузите фото для 3D моделирования.")
    bot.register_next_step_handler(message, handle_photo_modeling, bot)

def handle_photo_modeling(message, bot):
    if message.photo:
        photo = message.photo[-1].file_id
        if 'photos' not in user_data[_globals.gchat_id]:
            user_data[_globals.gchat_id]['photos'] = []  
        user_data[_globals.gchat_id]['photos'].append(photo)  
        send_buttons_after_photo_modeling(message, bot)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, загрузите фото по одному.")
        bot.register_next_step_handler(message, handle_phone_modeling, bot)

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
    # chat_id = message.hat.id
    if user_data[_globals.gchat_id]['photos']:
        user_data[_globals.gchat_id]['photos'].pop()  
    send_photo_request_modeling(message, bot)

def handle_add_photo_modeling(call, bot):
    message = call.message
    send_photo_request_modeling(message, bot)

def handle_next_step_modeling(call, bot):
    message = call.message
    bot.send_message(message.chat.id, "Пожалуйста, опишите требования к 3D модели.")
    bot.register_next_step_handler(message, handle_description_modeling, bot)

def handle_description_modeling(message,bot):
    description = message.text
    user_data[_globals.gchat_id]['description'] = description
    bot.send_message(message.chat.id, "Вы ввели следующее описание фронта работ:")
    bot.send_message(message.chat.id, description)
    bot.send_message(message.chat.id, "Пожалуйста, введите Ваше имя.")
    bot.register_next_step_handler(message, handle_name_modeling, bot)
 

def handle_name_modeling(message,bot):
    name = message.text
    user_data[_globals.gchat_id]['name'] = name
    bot.send_message(message.chat.id, "Вы ввели следующее имя:")
    bot.send_message(message.chat.id, name)
    bot.send_message(message.chat.id, "Пожалуйста, введите Ваш телефонный номер.")
    bot.register_next_step_handler(message, handle_phone_modeling, bot)
   
def handle_phone_modeling(message, bot):
    phone = message.text
    user_data[_globals.gchat_id]['phone'] = phone
    bot.send_message(message.chat.id, "Вы ввели следующий телефонный номер:")
    bot.send_message(message.chat.id, phone)
    send_confirmation_buttons_modeling(message, bot)  


def send_confirmation_buttons_modeling(message, bot):
    keyboard = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton(text=u'\U00002705 Подтвердить отправку', callback_data='confirm_send_modeling')
    keyboard.add(btn2)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)


def save_modeling_to_database(photos, description, name, phone, id):
    print("sm2db: in")
    try:
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1930",
        database="gm_robotics"
    )
        cursor = conn.cursor()
        print("sm2db: id=", id)

        # Преобразуем список photos в строку JSON
        photos_json = json.dumps(photos)

        # Всегда создаем новую запись для каждой заявки
        query = "INSERT INTO modeling (photos, description, name, telephone, unique_id_owner) VALUES (%s, %s, %s, %s, %s)"
        values = (photos_json, description, name, phone, id)
        cursor.execute(query, values)
        print("sm2db: inserted")
        conn.commit()
        print("sm2db: commited")
        
    except Exception as e:
        print(f"Ошибка при сохранении в базу данных: {e}")  # Логирование ошибки
    
        return False
    
    finally:
        if conn:
            cursor.close()
            conn.close()
    return True  # Возвращаем True, если дошли до этой точки без ошибок    

def send_application_modeling_to_owner(photos, description, name, phone):
    print("in send_application_to_owner")
    
        # Отправляем сообщение владельцу ссылки
    bot.send_message(_globals.gchat_id, f"\U0001F4DC Новая заявка от пользователя : {name}:")
    bot.send_message(_globals.gchat_id, f"\U0001F4DE Номер телефона : {phone}")
    bot.send_message(_globals.gchat_id, f"\U0000270F\U0000FE0F Описание : {description}")
   
    if photos:
        if len(photos) == 1:
            file_info = bot.get_file(photos[0])
            downloaded_file = bot.download_file(file_info.file_path)
            bot.send_photo(_globals.gchat_id, downloaded_file)
        else:
            media_group = []
            for photo in photos:
                file_info = bot.get_file(photo)
                downloaded_file = bot.download_file(file_info.file_path)
                media_group.append(telebot.types.InputMediaPhoto(downloaded_file))
            bot.send_media_group(_globals.gchat_id, media_group)
    
    print(f"Заявка отправлена владельцу с chat_id: {_globals.gchat_id}")
    return True 


def handle_confirm_send_modeling(call):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1930",
        database="gm_robotics"
    )
    cursor = conn.cursor()
    message = call.message
    chat_id = message.chat.id
    print("hcsm: fetching id from registration with chat_id=", (_globals.gchat_id))
    
    # 'select chat_id from registration where unique_id=?''   
    if _globals.gchat_id not in user_data:
        bot.answer_callback_query(call.id, "Отсутствуют необходимые данные. Пожалуйста, начните сначала.")
        return
    
    photos = user_data[_globals.gchat_id].get('photos', [])
    description = user_data[_globals.gchat_id].get('description', '')
    name = user_data[_globals.gchat_id].get('name', '')
    phone = user_data[_globals.gchat_id].get('phone', '')
    
    # Получаем значение unique_id из базы данных
    query = "SELECT id FROM registration WHERE chat_id = %s"
    values = (_globals.gchat_id,)
    cursor.execute(query, values)
    print("hcss: executed")
    result = cursor.fetchone()
    print("hcss: fetched")
    conn.close()
    
    if result is not None:
        print("hcss: calling sm2db(.. ?)", (result[0]))
        if save_modeling_to_database(photos, description, name, phone, result[0]):
            send_application_modeling_to_owner(photos, description, name, phone)  
            bot.answer_callback_query(call.id, "Заявка успешно отправлена.")
            bot.send_message(message.chat.id, "С вами свяжутся в ближайшее время. Чтобы создать новое обращение, нажмите /start.")
        else:
            bot.send_message(chat_id, "Произошла ошибка при сохранении заявки.")
            bot.answer_callback_query(call.id, "Ошибка при отправке заявки.")
    else:
        bot.answer_callback_query(call.id, "Не найден соответствующий идентификатор пользователя (unique_id) в базе данных.")
        bot.send_message(message.chat.id,"Нажмите /start")

# def handle_confirm_send_modeling(call):
#     message = call.message
#     chat_id = message.chat.id
#     photos = user_data[chat_id]['photos']
#     description = user_data[chat_id]['description']
    
#     if 'name' in user_data[chat_id]:
#         name = user_data[chat_id]['name']
#         send_confirmation_modeling(message, bot, photos, description, name)
#     else:
#         bot.send_message(chat_id, "Пожалуйста, введите Ваше имя.")
#         bot.register_next_step_handler(message, handle_name_modeling, bot) 

# def send_confirmation_modeling(message,bot, photos, description,name):
#     bot.send_message(message.chat.id, "Данные отправлены:")
#     for photo in photos:
#         bot.send_photo(message.chat.id, photo)
#     bot.send_message(message.chat.id, f"Фронт работ: {description}")
#     bot.send_message(message.chat.id, f"Фронт работ: {name}")
#     bot.send_message(message.chat.id, "С вами свяжутся в ближайшее время. Чтобы создать новое обращение, нажмите /start.")
#     del user_data[message.chat.id]               

# @bot.callback_query_handler(func=lambda call: call.data == 'confirm_send_modeling')
# def handle_confirm_send_modeling(call):
#     message = call.message
#     chat_id = message.chat.id
#     photos = user_data[chat_id]['photos']
#     description = user_data[chat_id]['description']
#     name = user_data[chat_id]['name']
#     phone = user_data[chat_id]['phone']
#     send_confirmation_modeling(message, bot, photos, description,name,phone)

#     conn_thread = sqlite3.connect('gmbot.db')
#     c_thread = conn_thread.cursor()

#     c_thread.execute("INSERT INTO modeling (photos, description, name, telephone) VALUES (?, ?, ?, ?)",
#                      (','.join(photos), description, name, phone))
#     conn_thread.commit()
    
#     # Закрытие соединения и курсора в текущем потоке
#     c_thread.close()
#     conn_thread.close()

# def send_confirmation_modeling(message, bot, photos, description, name, phone):
#     bot.send_message(message.chat.id, "Данные отправлены:")
#     for photo in photos:
#         bot.send_photo(message.chat.id, photo)
#     bot.send_message(message.chat.id, f"Фронт работ: {description}")
#     bot.send_message(message.chat.id, f"Имя: {name}")
#     bot.send_message(message.chat.id, f"Телефонный номер: {phone}")
#     bot.send_message(message.chat.id, "С вами свяжутся в ближайшее время. Чтобы создать новое обращение, нажмите /start.")
#     del user_data[message.chat.id]