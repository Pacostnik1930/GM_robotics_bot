import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('7138089393:AAEoBSwwCzVYOaUDEQdv6Vv0ILiaR-LwZ5k')

user_data = {}

user_data = {}

conn = sqlite3.connect('gmbot.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS printing
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             documents TEXT,
             description TEXT,
             name TEXT,
             telephone TEXT)''')
conn.commit()




def handle_3d_print(message,bot):
    markup = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton('Да', callback_data='has_3d_model')
    btn_no = types.InlineKeyboardButton('Нет', callback_data='no_3d_model')
    markup.row(btn_yes, btn_no)
    bot.send_message(message.chat.id, "Есть ли у вас 3D модель для печати?", reply_markup=markup)

def handle_no_3d_model(call,bot):
        markup = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton('Назад', callback_data='back_to_main_menu')
        markup.row(btn_back)
        bot.send_message(call.message.chat.id, "Рекомендуем вам сначала создать 3D модель.", reply_markup=markup)


def handle_has_3d_model(message, bot):
    bot.send_message(message.chat.id, "Пожалуйста, загрузите файл для печати.")
    bot.register_next_step_handler(message, handle_file_printing, bot)

def handle_printing(message, bot):
    chat_id = message.chat.id
    user_data[chat_id] = {'documents': []}
    handle_has_3d_model(message, bot)    

def handle_file_printing(message, bot):
    chat_id = message.chat.id
    if chat_id not in user_data:
        user_data[chat_id] = {}
    if message.document:
        file_id = message.document.file_id
        if 'documents' not in user_data[chat_id]:
            user_data[chat_id]['documents'] = []
        user_data[chat_id]['documents'].append(file_id)
        send_buttons_after_file_printing(message, bot)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, загрузите файл по одному.")
        bot.register_next_step_handler(message, handle_file_printing, bot)
    

def send_buttons_after_file_printing(message, bot):
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Назад', callback_data='back_to_file_printing')
    keyboard.row(btn1)
    btn2 = types.InlineKeyboardButton(text='Далее', callback_data='next_step_printing')
    keyboard.row(btn2)
    btn3 = types.InlineKeyboardButton(text='Добавить еще файл', callback_data='add_file_printing')
    keyboard.row(btn3)
    bot.send_message(message.chat.id, "Файл получен. Выберите действие:", reply_markup=keyboard)

def handle_back_to_file_printing(call, bot):
    message = call.message
    chat_id = message.chat.id
    if user_data[chat_id]['documents']:
        user_data[chat_id]['documents'].pop()  # Удаляем последнее загруженное фото
    handle_has_3d_model(message, bot)
        
def handle_add_file_printing(call, bot):
    message = call.message
    handle_has_3d_model(message, bot)    

def handle_next_step_printing(call, bot):
    message = call.message
    bot.send_message(message.chat.id, "Пожалуйста, опишите фронт работ.")
    bot.register_next_step_handler(message, handle_description_printing, bot) 


def handle_description_printing(message,bot):
    chat_id = message.chat.id
    description = message.text
    user_data[chat_id]['description'] = description
    bot.send_message(chat_id, "Вы ввели следующее описание фронта работ:")
    bot.send_message(chat_id, description)
    bot.send_message(chat_id, "Пожалуйста, введите Ваше имя.")
    bot.register_next_step_handler(message, handle_name_printing, bot)

def handle_name_printing(message,bot):
    chat_id = message.chat.id
    name = message.text
    user_data[chat_id]['name'] = name
    bot.send_message(chat_id, "Вы ввели следующее имя:")
    bot.send_message(chat_id, name)
    bot.send_message(chat_id, "Пожалуйста, введите Ваш телефонный номер.")
    bot.register_next_step_handler(message, handle_phone_printing, bot)    
 
def handle_phone_printing(message, bot):
    chat_id = message.chat.id
    phone = message.text
    user_data[chat_id]['phone'] = phone
    bot.send_message(chat_id, "Вы ввели следующий телефонный номер:")
    bot.send_message(chat_id, phone)
    send_confirmation_buttons_printing(message, bot) 


def send_confirmation_buttons_printing(message, bot):
    keyboard = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton(text='Подтвердить отправку', callback_data='confirm_send_printing')
    keyboard.add( btn2)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)

def handle_confirm_send_printing(call):
    message = call.message
    chat_id = message.chat.id
    documents = user_data[chat_id]['documents']
    description = user_data[chat_id]['description']
    
    if 'name' in user_data[chat_id]:
        name = user_data[chat_id]['name']
        send_confirmation_printing(message, bot, documents, description, name)
    else:
        bot.send_message(chat_id, "Пожалуйста, введите Ваше имя.")
        bot.register_next_step_handler(message, handle_name_printing, bot)    

@bot.callback_query_handler(func=lambda call: call.data == 'confirm_send_printing')
def handle_confirm_send_printing(call):
    message = call.message
    chat_id = message.chat.id
    documents = user_data[chat_id]['documents']
    description = user_data[chat_id]['description']
    name = user_data[chat_id]['name']
    phone = user_data[chat_id]['phone']
    send_confirmation_printing(message, bot, documents, description,name,phone)

    conn_thread = sqlite3.connect('gmbot.db')
    c_thread = conn_thread.cursor()

    c_thread.execute("INSERT INTO printing (documents, description, name, telephone) VALUES (?, ?, ?, ?)",
                     (','.join(documents), description, name, phone))
    conn_thread.commit()
    
    # Закрытие соединения и курсора в текущем потоке
    c_thread.close()
    conn_thread.close()   


def send_confirmation_printing(message,bot, documents, description,name,phone):
    bot.send_message(message.chat.id, "Данные отправлены:")
    for document in documents:
        bot.send_document(message.chat.id, document)
    bot.send_message(message.chat.id, f"Фронт работ: {description}")
    bot.send_message(message.chat.id, f"Фронт работ: {name}")
    bot.send_message(message.chat.id, f"Телефонный номер: {phone}")
    bot.send_message(message.chat.id, "С вами свяжутся в ближайшее время. Чтобы создать новое обращение, нажмите /start.")
    del user_data[message.chat.id]