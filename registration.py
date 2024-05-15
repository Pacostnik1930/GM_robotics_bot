from telebot import types
import telebot
import sqlite3
import mysql.connector

bot = telebot.TeleBot('7138089393:AAEoBSwwCzVYOaUDEQdv6Vv0ILiaR-LwZ5k')

user_data = {}


def handle_registration(message,bot):
    chat_id = message.chat.id
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1930",
        database="gm_robotics"
    )
    cursor = conn.cursor()
    query = "SELECT unique_id FROM registration WHERE chat_id = %s" 
    values = (chat_id,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        unique_link = result[0]
        bot.send_message(chat_id, f"Вы уже зарегистрированы. Ваша уникальная ссылка: {unique_link}")
    # else:
    #     keyboard = types.InlineKeyboardMarkup(row_width=1)
    #     btn_reg = types.InlineKeyboardButton('Авторизация по Telegram ID', callback_data='Авторизация')
    #     btn_back = types.InlineKeyboardButton('Назад', callback_data='Назад')
    #     keyboard.add(btn_reg, btn_back)
    # bot.send_message(chat_id, "Нажмите на кнопку 'Авторизация по Telegram ID' для авторизации.", reply_markup=keyboard)

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

def generate_unique_link(unique_id):
    return f"https://t.me/GMroboticsBot?start={unique_id}"

def handle_confirmation(call, bot):
    _, username, name = call.data.split('_')
    
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1930",
        database="gm_robotics"
    )
    cursor = conn.cursor()
    
    # Проверяем наличие уникальной ссылки для пользователя
    query = "SELECT unique_id FROM registration WHERE name = %s AND chat_id = %s" 
    values = (name, call.message.chat.id)
    cursor.execute(query,values)
    existing_link = cursor.fetchone()
    
    if existing_link:
        bot.send_message(call.message.chat.id, f"Вы уже зарегистрированы. Ваша уникальная ссылка: {existing_link[0]}")
    else:
        # Проверяем отсутствие записи с таким chat_id
        query = "SELECT * FROM registration WHERE chat_id = %s" 
        values = (call.message.chat.id,)
        cursor.execute(query,values)
        existing_registration = cursor.fetchone()
        
        if not existing_registration:
            # Генерируем новую уникальную ссылку
            query = "SELECT MAX(id) FROM registration"
            cursor.execute(query)
            result = cursor.fetchone()
            count = result[0] if result[0] is not None else 0
            unique_id = str(count + 1)
            unique_link = generate_unique_link(unique_id)

            # Добавляем новую уникальную ссылку в базу данных
            query = "INSERT INTO registration (name, chat_id, unique_id) VALUES (%s, %s, %s)"
            values = (name, call.message.chat.id, unique_link)
            cursor.execute(query,values)
            conn.commit()
            
            bot.send_message(call.message.chat.id, f"Ваша уникальная ссылка: {unique_link}")
        else:
            # Получаем существующую уникальную ссылку для пользователя
            query = "SELECT unique_id FROM registration WHERE chat_id = %s " 
            values = (call.message.chat.id,)
            cursor.execute(query,values)
            existing_link = cursor.fetchone()
            
            if existing_link:
                bot.send_message(call.message.chat.id, f"У вас уже есть уникальная ссылка в нашей системе: {existing_link[0]}")
            else:
                bot.send_message(call.message.chat.id, "У вас уже есть регистрация, но уникальная ссылка не найдена.")

    cursor.close()
    conn.close()