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
             name TEXT,
             telephone TEXT,            
             chat_id INTEGER,
             user_id INTEGER,
             FOREIGN KEY (user_id) REFERENCES registration (id))''')
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
    btn2 = types.InlineKeyboardButton(text='Подтвердить отправку', callback_data='confirm_send_scanning')
    keyboard.add( btn2)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)


def save_scanning_to_database(chat_id, photos, description, name, phone, user_id):
    try:
        conn = sqlite3.connect('gmbot.db')
        cursor = conn.cursor()

        # Преобразуем список photos в строку JSON
        photos_json = json.dumps(photos)

        # Всегда создаем новую запись для каждой заявки
        cursor.execute("INSERT INTO scanning (chat_id, photos, description, name, telephone, user_id) VALUES (?, ?, ?, ?, ?, ?)",
                       (chat_id, photos_json, description, name, phone, user_id))

        conn.commit()
    except Exception as e:
        print(f"Ошибка при сохранении в базу данных: {e}")  # Логирование ошибки
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()
    return True  # Возвращаем True, если дошли до этой точки без ошибок
    

def send_application_to_owner(owner_chat_id, photos, description, name, phone):
    # Сначала отправляем текстовое сообщение с описанием, именем и телефоном
    message_text = f"Новая заявка:\n\nОписание: {description}\nИмя: {name}\nТелефон: {phone}"
    bot.send_message(owner_chat_id, message_text)
    
    # Теперь отправляем фотографии
    if photos:
        if len(photos) == 1:
            # Если фотография одна, используем метод send_photo
            bot.send_photo(owner_chat_id, photos[0])
        else:
            # Если фотографий несколько, используем метод send_media_group
            media_group = [telebot.types.InputMediaPhoto(photo) for photo in photos]
            bot.send_media_group(owner_chat_id, media_group)

    
    # owner_chat_id = '535373696'
    # photos = user_data[chat_id]['photos']
    # description = user_data[chat_id]['description']
    # name = user_data[chat_id]['name']
    # phone = user_data[chat_id]['phone']


# После сохранения данных в базу данных вызываем функцию отправки
    # send_application_to_owner(owner_chat_id, photos, description, name, phone)        

    
@bot.callback_query_handler(func=lambda call: call.data == 'confirm_send_scanning')
def handle_confirm_send_scanning(call):
    message = call.message
    chat_id = message.chat.id

    # Проверки на наличие данных
    if chat_id not in user_data or not all(k in user_data[chat_id] for k in ('photos', 'description', 'name', 'phone')):
        bot.answer_callback_query(call.id, "Отсутствуют необходимые данные. Пожалуйста, начните сначала.")
        return

    # Извлечение данных пользователя
    photos = user_data[chat_id]['photos']
    description = user_data[chat_id]['description']
    name = user_data[chat_id]['name']
    phone = user_data[chat_id]['phone']
    user_id = chat_id

    # Сохранение в базу данных и отправка заявки
    if save_scanning_to_database(chat_id, photos, description, name, phone,user_id):
        bot.send_message(chat_id, "Ваша заявка на сканирование отправлена.")
        # Здесь предполагается, что owner_chat_id - это ID админа/владельца для уведомления о новой заявке
        owner_chat_id = '535373696'
        send_application_to_owner(owner_chat_id, photos, description, name, phone)
        bot.answer_callback_query(call.id, "Заявка успешно отправлена.")
    else:
        bot.send_message(chat_id, "Произошла ошибка при сохранении заявки.")
        bot.answer_callback_query(call.id, "Ошибка при отправке заявки.")

def send_confirmation_scanning(message, bot, photos, description, name,phone):
    bot.send_message(message.chat.id, "Данные отправлены:")
    for photo in photos:
        bot.send_photo(message.chat.id, photo)
    bot.send_message(message.chat.id, f"Фронт работ: {description}")
    bot.send_message(message.chat.id, f"Имя: {name}")
    bot.send_message(message.chat.id, f"Телефонный номер: {phone}")
    bot.send_message(message.chat.id, "С вами свяжутся в ближайшее время. Чтобы создать новое обращение, нажмите /start.")
    del user_data[message.chat.id]   


    