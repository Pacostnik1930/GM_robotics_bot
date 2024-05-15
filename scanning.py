import json
import telebot
from telebot import types
import sqlite3
import _globals
import mysql.connector

bot = telebot.TeleBot('7138089393:AAEoBSwwCzVYOaUDEQdv6Vv0ILiaR-LwZ5k')

user_data = {}
button_clicked = False

def handle_scanning(message, bot):
    # gchat_id = get_gchat_id()
    user_data[_globals.gchat_id] = {'photos': []}
    send_photo_request_scanning(message, bot)

def send_photo_request_scanning(message, bot):
    bot.send_message(message.chat.id, "Пожалуйста, загрузите фото для сканирования.")
    bot.register_next_step_handler(message, handle_photo_scanning, bot)

def handle_photo_scanning(message, bot):
    if message.photo:
        photo = message.photo[-1].file_id
        if 'photos' not in user_data[_globals.gchat_id]:
            user_data[_globals.gchat_id]['photos'] = []  
        user_data[_globals.gchat_id]['photos'].append(photo)  
        send_buttons_after_photo_scanning(message, bot)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, загрузите фото по одному.")
        bot.register_next_step_handler(message, handle_photo_scanning, bot)

def send_buttons_after_photo_scanning(message, bot):
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Назад', callback_data='back_to_photo_scanning')
    keyboard.row(btn1)
    btn2 = types.InlineKeyboardButton(text='Далее', callback_data='next_step_scanning')
    keyboard.row(btn2)
    btn3 = types.InlineKeyboardButton(text='Добавить еще фото', callback_data='add_photo_scanning')
    keyboard.row(btn3)
    bot.send_message(message.chat.id, "Фото получено. Выберите действие:", reply_markup=keyboard)

def handle_back_to_photo_scanning(call, bot):
    message = call.message
    # chat_id = message.hat.id
    if user_data[_globals.gchat_id]['photos']:
        user_data[_globals.gchat_id]['photos'].pop()  
    send_photo_request_scanning(message, bot)

def handle_add_photo_scanning(call, bot):
    message = call.message
    send_photo_request_scanning(message, bot)

def handle_next_step_scanning(call, bot):
    message = call.message
    bot.send_message(message.chat.id, "Пожалуйста, опишите фронт работ.")
    bot.register_next_step_handler(message, handle_description_scanning, bot)

def handle_description_scanning(message,bot):  
    description = message.text
    user_data[_globals.gchat_id]['description'] = description
    bot.send_message(message.chat.id, "Вы ввели следующее описание фронта работ:")
    bot.send_message(message.chat.id, description)
    bot.send_message(message.chat.id, "Пожалуйста, введите Ваше имя.")
    bot.register_next_step_handler(message, handle_name_scanning, bot)
 
def handle_name_scanning(message,bot):
    name = message.text
    user_data[_globals.gchat_id]['name'] = name
    bot.send_message(message.chat.id, "Вы ввели следующее имя:")
    bot.send_message(message.chat.id, name)
    bot.send_message(message.chat.id, "Пожалуйста, введите Ваш телефонный номер.")
    bot.register_next_step_handler(message, handle_phone_scanning, bot)

def handle_phone_scanning(message, bot):
    phone = message.text
    user_data[_globals.gchat_id]['phone'] = phone
    bot.send_message(message.chat.id, "Вы ввели следующий телефонный номер:")
    bot.send_message(message.chat.id, phone)
    send_confirmation_buttons_scanning(message, bot)

def send_confirmation_buttons_scanning(message, bot):
    global button_clicked
    if not button_clicked:
        keyboard = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton(text=u'\U00002705 Подтвердить отправку', callback_data=f"confirm_send_scanning_")
        keyboard.add(btn2)
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)
        button_clicked = True
        
def save_scanning_to_database(photos, description, name, phone, id):
    print("ss2db: in")
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1930",
            database="gm_robotics"
        )
        cursor = conn.cursor()
        print("ss2db: id=", id)

        photos_json = json.dumps(photos)
        query = "INSERT INTO scanning (photos, description, name, telephone, unique_id_owner) VALUES (%s, %s, %s, %s, %s)"
        values = (photos_json, description, name, phone, id)
        cursor.execute(query, values)
        print("ss2db: inserted")
        conn.commit()
        print("ss2db: commited")   
    except Exception as e:
        print(f"Ошибка при сохранении в базу данных: {e}")  # Логирование ошибки
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()
    return True 
      

def send_application_to_owner(photos, description, name, phone):
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

def handle_confirm_send_scanning(call):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1930",
        database="gm_robotics"
    )
    cursor = conn.cursor()
    message = call.message
    chat_id = message.chat.id
    # user_states[chat_id] = '3Д сканирование'
    print("hcss: fetching id from registration with chat_id=", (_globals.gchat_id))
    # 'select chat_id from registration where unique_id=?''   
    if _globals.gchat_id not in user_data:
        bot.answer_callback_query(call.id, "Отсутствуют необходимые данные. Пожалуйста, начните сначала.")
        return
    photos = user_data[_globals.gchat_id].get('photos', [])
    description = user_data[_globals.gchat_id].get('description', '')
    name = user_data[_globals.gchat_id].get('name', '')
    phone = user_data[_globals.gchat_id].get('phone', '')

    query = "SELECT id FROM registration WHERE chat_id = %s"
    values = (_globals.gchat_id,)
    cursor.execute(query, values)
    print("hcss: executed")
    result = cursor.fetchone()
    print("hcss: fetched")
    conn.close()
    if result is not None:
        print("hcss: calling ss2db(.. ?)", (result[0]))
        # unique_id = result[0]  # Получаем значение unique_id из результата запроса
        if save_scanning_to_database(photos, description, name, phone, result[0]):
            send_application_to_owner(photos, description, name, phone)  
            bot.answer_callback_query(call.id, "Заявка успешно отправлена.")
            bot.send_message(message.chat.id, "С вами свяжутся в ближайшее время. Чтобы создать новое обращение, нажмите /start.")
        else:
            bot.send_message(chat_id, "Произошла ошибка при сохранении заявки.")
            bot.answer_callback_query(call.id, "Ошибка при отправке заявки.")
    else:
        bot.answer_callback_query(call.id, "Не найден соответствующий идентификатор пользователя (unique_id) в базе данных.")
        bot.send_message(message.chat.id,"Нажмите /start")

# def handle_confirm_send_scanning(call):
#     conn = sqlite3.connect('gmbot.db')
#     cursor = conn.cursor()
#     message = call.message
#     chat_id = message.chat.id
#     # user_states[chat_id] = '3Д сканирование'
#     print("hcss: fetching id from registration with chat_id=", (_globals.gchat_id))
    
#     # 'select chat_id from registration where unique_id=?''   
#     if _globals.gchat_id not in user_data:
#         bot.answer_callback_query(call.id, "Отсутствуют необходимые данные. Пожалуйста, начните сначала.")
#         return
    
#     photos = user_data[_globals.gchat_id].get('photos', [])
#     description = user_data[_globals.gchat_id].get('description', '')
#     name = user_data[_globals.gchat_id].get('name', '')
#     phone = user_data[_globals.gchat_id].get('phone', '')
    
#     # Получаем значение unique_id из базы данных
#     cursor.execute("SELECT id FROM registration WHERE chat_id = ?", (_globals.gchat_id,))
#     print("hcss: executed")
#     result = cursor.fetchone()
#     print("hcss: fetched")
#     conn.close()
    
#     if result is not None:
#         print("hcss: calling ss2db(.. ?)", (result[0]))
#         # unique_id = result[0]  # Получаем значение unique_id из результата запроса
#         if save_scanning_to_database(photos, description, name, phone, result[0]):
#             send_application_to_owner(photos, description, name, phone)  
#             bot.answer_callback_query(call.id, "Заявка успешно отправлена.")
#             bot.send_message(message.chat.id, "С вами свяжутся в ближайшее время. Чтобы создать новое обращение, нажмите /start.")
#         else:
#             bot.send_message(chat_id, "Произошла ошибка при сохранении заявки.")
#             bot.answer_callback_query(call.id, "Ошибка при отправке заявки.")
#     else:
#         bot.answer_callback_query(call.id, "Не найден соответствующий идентификатор пользователя (unique_id) в базе данных.")
#         bot.send_message(message.chat.id,"Нажмите /start")
