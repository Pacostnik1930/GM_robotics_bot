
import json
import telebot
from telebot import types
import sqlite3


bot = telebot.TeleBot('7138089393:AAEoBSwwCzVYOaUDEQdv6Vv0ILiaR-LwZ5k')

user_data = {}


conn = sqlite3.connect('gmbot.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS scanning
             (id INTEGER PRIMARY KEY AUTOINCREMENT,      
             photos TEXT,
             description TEXT,
             unique_id_owner TEXT,   
             name TEXT,
             telephone TEXT,            
             FOREIGN KEY (unique_id_owner) REFERENCES registration (unique_id))''')

conn.commit()

def handle_scanning(message, bot):
    chat_id = message.chat.id
    user_data[chat_id] = {'photos': []}
    send_photo_request_scanning(message, bot)

def send_photo_request_scanning(message, bot):
    bot.send_message(message.chat.id, "Пожалуйста, загрузите фото для сканирования.")
    bot.register_next_step_handler(message, handle_photo_scanning, bot)

def handle_photo_scanning(message, bot):
    chat_id = message.chat.id
    if message.photo:
        photo = message.photo[-1].file_id
        if 'photos' not in user_data[chat_id]:
            user_data[chat_id]['photos'] = []  
        user_data[chat_id]['photos'].append(photo)  
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
    chat_id = message.hat.id
    if user_data[chat_id]['photos']:
        user_data[chat_id]['photos'].pop()  
    send_photo_request_scanning(message, bot)

def handle_add_photo_scanning(call, bot):
    message = call.messagec
    send_photo_request_scanning(message, bot)

def handle_next_step_scanning(call, bot):
    message = call.message
    bot.send_message(message.chat.id, "Пожалуйста, опишите фронт работ.")
    bot.register_next_step_handler(message, handle_description_scanning, bot)

def handle_description_scanning(message,bot):
    chat_id = message.chat.id
    description = message.text
    user_data[chat_id]['description'] = description
    bot.send_message(chat_id, "Вы ввели следующее описание фронта работ:")
    bot.send_message(chat_id, description)
    bot.send_message(chat_id, "Пожалуйста, введите Ваше имя.")
    bot.register_next_step_handler(message, handle_name_scanning, bot)
 

def handle_name_scanning(message,bot):
    chat_id = message.chat.id
    name = message.text
    user_data[chat_id]['name'] = name
    bot.send_message(chat_id, "Вы ввели следующее имя:")
    bot.send_message(chat_id, name)
    bot.send_message(chat_id, "Пожалуйста, введите Ваш телефонный номер.")
    bot.register_next_step_handler(message, handle_phone_scanning, bot)

def handle_phone_scanning(message, bot):
    chat_id = message.chat.id
    phone = message.text
    user_data[chat_id]['phone'] = phone
    bot.send_message(chat_id, "Вы ввели следующий телефонный номер:")
    bot.send_message(chat_id, phone)
    send_confirmation_buttons_scanning(message, bot)

def send_confirmation_buttons_scanning(message, bot):
    keyboard = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton(text='Подтвердить отправку', callback_data=f"confirm_send_scanning_")
    keyboard.add( btn2)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)



def save_scanning_to_database(photos, description, name, phone,unique_id_owner):
    try:
        conn = sqlite3.connect('gmbot.db')
        cursor = conn.cursor()

        # Преобразуем список photos в строку JSON
        photos_json = json.dumps(photos)

        # Всегда создаем новую запись для каждой заявки
        cursor.execute("INSERT  INTO scanning (photos, description, name, telephone,unique_id_owner) VALUES (?, ?, ?, ?,?)",
                       (photos_json, description, name, phone,unique_id_owner))
        conn.commit()
        
    except Exception as e:
        print(f"Ошибка при сохранении в базу данных: {e}")  # Логирование ошибки
    
        return False
    
    finally:
        if conn:
            cursor.close()
            conn.close()
    return True  # Возвращаем True, если дошли до этой точки без ошибок
# create_trigger()    
# def create_trigger():
#     try:
#         conn = sqlite3.connect('gmbot.db')
#         cursor = conn.cursor()
#         cursor.execute('''CREATE TRIGGER IF NOT EXISTS set_scanning_is_owner
#                         AFTER INSERT ON scanning
#                         FOR EACH ROW
#                         BEGIN
#                             UPDATE scanning
#                             SET is_owner = (
#                                 SELECT is_owner FROM registration
#                                 WHERE registration.unique_id = NEW.unique_id
#                             )
#                             WHERE id = NEW.id ;
#                         END;''')
        
#         conn.commit()
#         print("Trigger created successfully.")
    
#     except Exception as e:
#         print(f"Error creating trigger: {e}")
#         conn.rollback()
    
#     finally:
#         if conn:
#             conn.close()
         
# def test_trigger():
#     try:
#         conn = sqlite3.connect('gmbot.db')
#         cursor = conn.cursor()
        
#         # Создаем временную запись в таблице registration
#         cursor.execute("INSERT OR IGNORE INTO registration (username, name, unique_id, chat_id) VALUES ('test_user', 'John Doe', 'TEST123', '12345')")
        
#         # Создаем временную запись в таблице scanning для активации триггера
#         cursor.execute("INSERT INTO scanning (description, name, telephone, unique_id) VALUES ('Test description', 'Test name', '123456789', 'TEST123')")
        
#         conn.commit()
#         print("Temporary records inserted successfully.")
    
#     except Exception as e:
#         print(f"Error inserting temporary records: {e}")
#         conn.rollback()
    
#     finally:
#         if conn:
#             conn.close()

# # Создаем триггер
# create_trigger()

# # Тестируем триггер добавлением временных записей
# test_trigger()            


# def send_application_to_owner(unique_id, photos, description, name, phone):
#     try:
#         conn = sqlite3.connect('gmbot.db')
#         cursor = conn.cursor()
#         cursor.execute("SELECT is_owner FROM registration WHERE unique_id = ? ", ( unique_id,))
#         result = cursor.fetchone()
#         print(result)
#         if result is not None:
#             is_owner = result[0]
#             message_text = f"Новая заявка:\n\nОписание: {description}\nИмя: {name}\nТелефон: {phone}"
#             bot.send_message(is_owner, message_text)
#             cursor.execute("UPDATE scanning SET is_owner = ? WHERE unique_id = ?", (is_owner, unique_id,))
#             conn.commit()
#             if photos:
#                 if len(photos) == 1:
#                     bot.send_photo(is_owner, photos[0])
#                 else:
#                     media_group = [telebot.types.InputMediaPhoto(photo) for photo in photos]
#                     bot.send_media_group(is_owner, media_group)
#         else:
#             print(f"Не найден хозяин ссылки для unique_id: {unique_id}")
#     except Exception as e:
#         print(f"Ошибка при отправке заявки владельцу: {e}")  # Логирование ошибки
#     finally:
#         if conn:
#             cursor.close()
#             conn.close()

# create_trigger()

    
# def send_application_to_owner(unique_id, photos, description, name, phone):
#     try:
#         conn = sqlite3.connect('gmbot.db')
#         cursor = conn.cursor()
#         cursor.execute("SELECT chat_id FROM registration WHERE unique_id = ?" ,(unique_id,) )
#         result = cursor.fetchone()
#         print(result)
        
        
#         if result is not None and result[0] is not None:
#             chat_id = result[0]
#             print(result)
#             print(f"Заявка отправлена владельцу с chat_id: {chat_id}")
#             message_text = f"Новая заявка:\n\nОписание: {description}\nИмя: {name}\nТелефон: {phone}"
#             bot.send_message(chat_id, message_text)
#             if photos:
#                 if len(photos) == 1:
#                         bot.send_photo(chat_id, photos[0])
#                 else:
#                         media_group = [telebot.types.InputMediaPhoto(photo) for photo in photos]
#                         bot.send_media_group(chat_id, media_group)
#         else:
#             print(f"Не найден хозяин ссылки для unique_id_owner: {unique_id}")
#             print(f"Поиск хозяина ссылки для unique_id_owner: {unique_id}")
#             cursor.execute("SELECT unique_id FROM registration WHERE unique_id = ?", (unique_id,))
#             result = cursor.fetchone()
#             print(f"Результат запроса: {result}")
#     except Exception as e:
#         print(f"Ошибка при отправке заявки владельцу: {e}")  # Логирование ошибки
#     finally:
#             if conn:
#                 cursor.close()
#                 conn.close()


def send_application_to_owner(unique_id, photos, description, name, phone):
    conn = sqlite3.connect('gmbot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM registration WHERE unique_id = ?", ( unique_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result is not None:
        owner_chat_id = result[0]  # Получаем chat_id владельца ссылки из результата запроса
        print(owner_chat_id)
        # Отправляем сообщение владельцу ссылки
        bot.send_message(owner_chat_id, f"Новая заявка от пользователя {name}:")
        bot.send_message(owner_chat_id, f"Номер телефона: {phone}")
        bot.send_message(owner_chat_id, f"Описание: {description}")
        
        # Отправляем фотографии владельцу ссылки
        if photos:
                 if len(photos) == 1:
                        bot.send_photo(owner_chat_id, photos[0])
                 else:
                         media_group = [telebot.types.InputMediaPhoto(photo) for photo in photos]
                         bot.send_media_group(owner_chat_id, media_group)
        
        print(f"Заявка отправлена владельцу с chat_id: {owner_chat_id}")
        return True
    else:
        print(f"Не найден владелец ссылки для unique_id: {unique_id}")
        return False
   




# def handle_confirm_send_scanning(call):
#     message = call.message
#     chat_id = message.chat.id
    
#     if chat_id not in user_data:
#         bot.answer_callback_query(call.id, "Отсутствуют необходимые данные. Пожалуйста, начните сначала.")
#         return
    
#     missing_keys = [k for k in ('photos', 'description', 'name', 'phone', 'unique_id') if k not in user_data[chat_id]]
#     if missing_keys:
#         bot.answer_callback_query(call.id, f"Отсутствуют следующие данные: {', '.join(missing_keys)}. Пожалуйста, начните сначала.")
#         return
    
#     photos = user_data[chat_id]['photos']
#     description = user_data[chat_id]['description']
#     name = user_data[chat_id]['name']
#     phone = user_data[chat_id]['phone']
#     unique_id = user_data[chat_id]['unique_id']
    
#     # Получаем правильное значение unique_id из базы данных
#     conn = sqlite3.connect('gmbot.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT unique_id FROM registration WHERE unique_id LIKE ?", ("https://t.me/GMroboticsBot?start=" + unique_id,))
#     result = cursor.fetchone()
#     conn.close()
    
#     if result is not None:
#         unique_id_owner = result[0]  # Получаем значение unique_id из результата запроса
#         if save_scanning_to_database(photos, description, name, phone, unique_id_owner):
#             send_application_to_owner(unique_id, photos, description, name, phone)  
#             bot.answer_callback_query(call.id, "Заявка успешно отправлена.")
#         else:
#             bot.send_message(chat_id, "Произошла ошибка при сохранении заявки.")
#             bot.answer_callback_query(call.id, "Ошибка при отправке заявки.")
#     else:
#         bot.answer_callback_query(call.id, "Не найдена соответствующая ссылка в базе данных.")

def handle_confirm_send_scanning(call):
    message = call.message
    chat_id = message.chat.id
    
    if chat_id not in user_data:
        bot.answer_callback_query(call.id, "Отсутствуют необходимые данные. Пожалуйста, начните сначала.")
        return
    
    photos = user_data[chat_id].get('photos', [])
    description = user_data[chat_id].get('description', '')
    name = user_data[chat_id].get('name', '')
    phone = user_data[chat_id].get('phone', '')
    
    # Получаем значение unique_id из базы данных
    conn = sqlite3.connect('gmbot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT unique_id FROM registration WHERE chat_id = ?", (chat_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result is not None:
        unique_id = result[0]  # Получаем значение unique_id из результата запроса
        if save_scanning_to_database(photos, description, name, phone, unique_id):
            send_application_to_owner(unique_id, photos, description, name, phone)  
            bot.answer_callback_query(call.id, "Заявка успешно отправлена.")
        else:
            bot.send_message(chat_id, "Произошла ошибка при сохранении заявки.")
            bot.answer_callback_query(call.id, "Ошибка при отправке заявки.")
    else:
        bot.answer_callback_query(call.id, "Не найден соответствующий идентификатор пользователя (unique_id) в базе данных.")




def send_confirmation_scanning(message, bot, photos, description, name,phone):
    bot.send_message(message.chat.id, "Данные отправлены:")
    for photo in photos:
        bot.send_photo(message.chat.id, photo)
    bot.send_message(message.chat.id, f"Фронт работ: {description}")
    bot.send_message(message.chat.id, f"Имя: {name}")
    bot.send_message(message.chat.id, f"Телефонный номер: {phone}")
    bot.send_message(message.chat.id, "С вами свяжутся в ближайшее время. Чтобы создать новое обращение, нажмите /start.")
    del user_data[message.chat.id]      
    