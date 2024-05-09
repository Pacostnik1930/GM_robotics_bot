
# from telebot import types
# import telebot
# import sqlite3
# import uuid

# bot = telebot.TeleBot('7138089393:AAEoBSwwCzVYOaUDEQdv6Vv0ILiaR-LwZ5k')

# user_data = {}

# # Создание базы данных и таблицы для хранения информации о клиентах
# conn = sqlite3.connect('gmbot.db')
# cursor = conn.cursor()
# cursor.execute('''CREATE TABLE IF NOT EXISTS registration
#                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                    name TEXT,
#                    unique_id TEXT UNIQUE,  
#                    chat_id TEXT)''')
                  
# conn.commit()



# def handle_registration(message, bot):
#     chat_id = message.chat.id
#     conn = sqlite3.connect('gmbot.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT unique_id FROM registration WHERE chat_id = ?", (chat_id,))
#     result = cursor.fetchone()
#     cursor.close()
#     conn.close()

#     if result:
#         unique_link = result[0]
#         bot.send_message(chat_id, f"Вы уже зарегистрированы. Ваша уникальная ссылка: {unique_link}")
#     # else:
#     #     keyboard = types.InlineKeyboardMarkup(row_width=1)
#     #     btn_reg = types.InlineKeyboardButton('Авторизация по Telegram ID', callback_data='Авторизация')
#     #     btn_back = types.InlineKeyboardButton('Назад', callback_data='Назад')
#     #     keyboard.add(btn_reg, btn_back)
#     #     bot.send_message(chat_id, "Нажмите на кнопку 'Авторизация по Telegram ID' для авторизации.", reply_markup=keyboard)

# def handle_authorization(message, bot,unique_id):
#     chat_id = message.chat.id
#     bot.send_message(message.chat.id, "Введите ваше имя:")
#     bot.register_next_step_handler(message, lambda message: handle_name_input(message, chat_id)) 
#     chat_id = message.chat.id
#     conn = sqlite3.connect('gmbot.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT chat_id FROM registration WHERE unique_id = ?", (unique_id,))
#     result = cursor.fetchone()
#     conn.close()

#     if result:
#         owner_chat_id = result[0]
#         bot.send_message(chat_id, f"Вы перешли по ссылке от пользователя с ID: {owner_chat_id}")
#         user_data[chat_id] = {'unique_id': unique_id}
#         keyboard = types.InlineKeyboardMarkup(row_width=2)
#         btn8 = types.InlineKeyboardButton('Мне нужна услуга', callback_data='need_service')
#         btn9 = types.InlineKeyboardButton('Я оказываю услугу', callback_data='provide_a_service')
#         keyboard.add(btn8, btn9)
#         bot.send_message(chat_id, "Привет! Выберите раздел:", reply_markup=keyboard)
#     else:
#         bot.send_message(chat_id, "Неверная ссылка. Нажмите /start")
# def handle_name_input(message, chat_id):
#     name = message.text
#     chat_id = message.chat.id
#     keyboard = types.InlineKeyboardMarkup(row_width=1)
#     btn_confirm = types.InlineKeyboardButton('Подтвердить', callback_data=f'Подтвердить_{chat_id}_{name}')
#     btn_back = types.InlineKeyboardButton('Назад', callback_data='Назад')
#     keyboard.add(btn_confirm, btn_back)
#     bot.send_message(message.chat.id, f"Ваше имя: {name}. Нажмите 'Подтвердить' для отправки данных.", reply_markup=keyboard)       

# def generate_unique_link():
#     conn = sqlite3.connect('gmbot.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT COUNT(*) FROM registration")
#     count = cursor.fetchone()[0]
#     cursor.close()
#     conn.close()
#     # unique_id = str(count + 1).zfill(2)
#     unique_id = str(uuid.uuid4())
#     return f"https://t.me/GMroboticsBot?start={unique_id}"
   


# def handle_confirmation(call, bot):
#     data_parts = call.data.split('_')
#     if len(data_parts) >= 3:
#         chat_id = data_parts[1]
#         name = '_'.join(data_parts[2:])  # Объединяем оставшиеся части в имя
#         unique_link = generate_unique_link()
        
#         conn = sqlite3.connect('gmbot.db')
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO registration (chat_id, name, unique_id) VALUES (?, ?, ?)",
#                        (chat_id, name, unique_link))
#         conn.commit()
        
#         bot.send_message(chat_id, f"Ваша уникальная ссылка: {unique_link}")
#     else:
#         bot.send_message(chat_id, "Ошибка: неверный формат данных кнопки.")

from telebot import types
import telebot
import sqlite3
import uuid

bot = telebot.TeleBot('7138089393:AAEoBSwwCzVYOaUDEQdv6Vv0ILiaR-LwZ5k')

user_data = {}

# Создание базы данных и таблицы для хранения информации о клиентах
conn = sqlite3.connect('gmbot.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS registration
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   unique_id TEXT UNIQUE,  
                   chat_id TEXT)''')
                  
conn.commit()



def handle_registration(message, bot):
    chat_id = message.chat.id
    conn = sqlite3.connect('gmbot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT unique_id FROM registration WHERE chat_id = ?", (chat_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        unique_link = result[0]
        bot.send_message(chat_id, f"Вы уже зарегистрированы. Ваша уникальная ссылка: {unique_link}")
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        btn_reg = types.InlineKeyboardButton('Авторизация по Telegram ID', callback_data='Авторизация')
        btn_back = types.InlineKeyboardButton('Назад', callback_data='Назад')
        keyboard.add(btn_reg, btn_back)
        bot.send_message(chat_id, "Нажмите на кнопку 'Авторизация по Telegram ID' для авторизации.", reply_markup=keyboard)

def handle_authorization(message, bot):
    username = message.from_user.username
    bot.send_message(message.chat.id, "Введите ваше имя:")
    bot.register_next_step_handler(message, lambda message: handle_name_input(message, username)) 

def handle_name_input(message, username):
    name = message.text
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn_confirm = types.InlineKeyboardButton('Подтвердить', callback_data=f'Подтвердить_{username}_{name}')
    btn_back = types.InlineKeyboardButton('Назад', callback_data='Назад')
    keyboard.add(btn_confirm, btn_back)
    bot.send_message(message.chat.id, f"Ваше имя: {name}. Нажмите 'Подтвердить' для отправки данных.", reply_markup=keyboard)       

def generate_unique_link():
    conn = sqlite3.connect('gmbot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM registration")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    unique_id = str(count + 1)
    # unique_id = str(uuid.uuid4())
    return f"https://t.me/GMroboticsBot?start={unique_id}"
   

def handle_confirmation(call, bot):
    _, username, name = call.data.split('_')
    unique_link = generate_unique_link()
    chat_id = call.message.chat.id
    conn = sqlite3.connect('gmbot.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO registration (name, chat_id, unique_id) VALUES (?, ?, ?)",
              ( name, chat_id, unique_link))
    unique_id = cursor.lastrowid
    user_data[call.message.from_user.id] = unique_id
    conn.commit()
    cursor.close()
    conn.close()
    bot.send_message(call.message.chat.id, f"Ваша уникальная ссылка: {unique_link}")