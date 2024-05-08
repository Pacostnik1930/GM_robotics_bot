import json
import telebot
from telebot import types
import sqlite3
import _globals

bot = telebot.TeleBot('7138089393:AAEoBSwwCzVYOaUDEQdv6Vv0ILiaR-LwZ5k')

user_data = {}

# conn = sqlite3.connect('gmbot.db')
# c = conn.cursor()
# c.execute('''CREATE TABLE IF NOT EXISTS printing
#              (id INTEGER PRIMARY KEY AUTOINCREMENT,
#              documents TEXT,
#              description TEXT,
#              name TEXT,
#              telephone TEXT)''')
# conn.commit()




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
    user_data[_globals.gchat_id] = {'documents': []}
    handle_has_3d_model(message, bot)    

def handle_file_printing(message, bot):
    if _globals.gchat_id not in user_data:
            user_data[_globals.gchat_id] = {}

    if message.document:
        file = message.document.file_id
        if 'documents' not in user_data[_globals.gchat_id]:
            user_data[_globals.gchat_id]['documents'] = []
        user_data[_globals.gchat_id]['documents'].append(file)
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
    if user_data[_globals.gchat_id]['documents']:
        user_data[_globals.gchat_id]['documents'].pop()  # Удаляем последнее загруженное фото
    handle_has_3d_model(message, bot)
        
def handle_add_file_printing(call, bot):
    message = call.message
    handle_has_3d_model(message, bot)    

def handle_next_step_printing(call, bot):
    message = call.message
    bot.send_message(message.chat.id, "Пожалуйста, опишите фронт работ.")
    bot.register_next_step_handler(message, handle_description_printing, bot) 


def handle_description_printing(message,bot):
    description = message.text
    user_data[_globals.gchat_id]['description'] = description
    bot.send_message(_globals.gchat_id, "Вы ввели следующее описание фронта работ:")
    bot.send_message(_globals.gchat_id, description)
    bot.send_message(_globals.gchat_id, "Пожалуйста, введите Ваше имя.")
    bot.register_next_step_handler(message, handle_name_printing, bot)

def handle_name_printing(message,bot):
    name = message.text
    user_data[_globals.gchat_id]['name'] = name
    bot.send_message(_globals.gchat_id, "Вы ввели следующее имя:")
    bot.send_message(_globals.gchat_id, name)
    bot.send_message(_globals.gchat_id, "Пожалуйста, введите Ваш телефонный номер.")
    bot.register_next_step_handler(message, handle_phone_printing, bot)    
 
def handle_phone_printing(message, bot):
    phone = message.text
    user_data[_globals.gchat_id]['phone'] = phone
    bot.send_message(_globals.gchat_id, "Вы ввели следующий телефонный номер:")
    bot.send_message(_globals.gchat_id, phone)
    send_confirmation_buttons_printing(message, bot) 


def send_confirmation_buttons_printing(message, bot):
    keyboard = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton(text='Подтвердить отправку', callback_data='confirm_send_printing')
    keyboard.add( btn2)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)


def save_print_to_database(files, description, name, phone, id):
    print("ss2db: in")
    try:
        conn = sqlite3.connect('gmbot.db')
        cursor = conn.cursor()
        print("ss2db: id=", id)

        # Преобразуем список photos в строку JSON
        documents_json = json.dumps(files)

        # Всегда создаем новую запись для каждой заявки
        cursor.execute("INSERT INTO printing (files, description, name, telephone, unique_id_owner) VALUES (?, ?, ?, ?,?)",
                       (documents_json, description, name, phone, id))
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
    return True  # Возвращаем True, если дошли до этой точки без ошибок

def send_application_print_to_owner(files, description, name, phone):
    print("in send_application_to_owner")
    
        # Отправляем сообщение владельцу ссылки
    bot.send_message(_globals.gchat_id, f"Новая заявка от пользователя {name}:")
    bot.send_message(_globals.gchat_id, f"Номер телефона: {phone}")
    bot.send_message(_globals.gchat_id, f"Описание: {description}")
   
    if files:
        if len(files) == 1:
            file_info = bot.get_file(files[0])
            file_name = file_info.file_path.split('/')[-1]  # Получаем имя файла из пути
            file_size = file_info.file_size
            if file_size <= 50 * 1024 * 1024:  # 500 MB
                downloaded_file = bot.download_file(file_info.file_path)
                bot.send_document(_globals.gchat_id, downloaded_file, visible_file_name=file_name)
            else:
                bot.send_message(_globals.gchat_id, "Файл слишком большой для отправки.")
        else:
            for file in files:
                file_info = bot.get_file(file)
                file_name = file_info.file_path.split('/')[-1]  # Получаем имя файла из пути
                downloaded_file = bot.download_file(file_info.file_path)
                # media_group.append(telebot.types.InputMediaDocument(downloaded_file, visible_file_name=file_name))
            bot.send_document(_globals.gchat_id, downloaded_file, visible_file_name=file_name)
    print(f"Заявка отправлена владельцу с chat_id: {_globals.gchat_id}")
    return True

def handle_confirm_send_printing(call):
    conn = sqlite3.connect('gmbot.db')
    cursor = conn.cursor()
    message = call.message
    chat_id = message.chat.id
    # user_states[chat_id] = '3Д сканирование'
    print("hcss: fetching id from registration with chat_id=", (_globals.gchat_id))
    
    # 'select chat_id from registration where unique_id=?''   
    if _globals.gchat_id not in user_data:
        bot.answer_callback_query(call.id, "Отсутствуют необходимые данные. Пожалуйста, начните сначала.")
        return
    
    files = user_data[_globals.gchat_id].get('documents', [])
    description = user_data[_globals.gchat_id].get('description', '')
    name = user_data[_globals.gchat_id].get('name', '')
    phone = user_data[_globals.gchat_id].get('phone', '')
    
    # Получаем значение unique_id из базы данных
    cursor.execute("SELECT id FROM registration WHERE chat_id = ?", (_globals.gchat_id,))
    print("hcss: executed")
    result = cursor.fetchone()
    print("hcss: fetched")
    conn.close()
    
    if result is not None:
        print("hcss: calling ss2db(.. ?)", (result[0]))
        # unique_id = result[0]  # Получаем значение unique_id из результата запроса
        if save_print_to_database(files, description, name, phone, result[0]):
            send_application_print_to_owner(files, description, name, phone)  
            bot.answer_callback_query(call.id, "Заявка успешно отправлена.")
        else:
            bot.send_message(chat_id, "Произошла ошибка при сохранении заявки.")
            bot.answer_callback_query(call.id, "Ошибка при отправке заявки.")
    else:
        bot.answer_callback_query(call.id, "Не найден соответствующий идентификатор пользователя (unique_id) в базе данных.")

# def handle_confirm_send_printing(call):
#     message = call.message
#     chat_id = message.chat.id
#     documents = user_data[chat_id]['documents']
#     description = user_data[chat_id]['description']
    
#     if 'name' in user_data[chat_id]:
#         name = user_data[chat_id]['name']
#         send_confirmation_printing(message, bot, documents, description, name)
#     else:
#         bot.send_message(chat_id, "Пожалуйста, введите Ваше имя.")
#         bot.register_next_step_handler(message, handle_name_printing, bot)    

# @bot.callback_query_handler(func=lambda call: call.data == 'confirm_send_printing')
# def handle_confirm_send_printing(call):
#     message = call.message
#     chat_id = message.chat.id
#     documents = user_data[chat_id]['documents']
#     description = user_data[chat_id]['description']
#     name = user_data[chat_id]['name']
#     phone = user_data[chat_id]['phone']
#     send_confirmation_printing(message, bot, documents, description,name,phone)

#     conn_thread = sqlite3.connect('gmbot.db')
#     c_thread = conn_thread.cursor()

#     c_thread.execute("INSERT INTO printing (documents, description, name, telephone) VALUES (?, ?, ?, ?)",
#                      (','.join(documents), description, name, phone))
#     conn_thread.commit()
    
#     # Закрытие соединения и курсора в текущем потоке
#     c_thread.close()
#     conn_thread.close()   


# def send_confirmation_printing(message,bot, documents, description,name,phone):
#     bot.send_message(message.chat.id, "Данные отправлены:")
#     for document in documents:
#         bot.send_document(message.chat.id, document)
#     bot.send_message(message.chat.id, f"Фронт работ: {description}")
#     bot.send_message(message.chat.id, f"Фронт работ: {name}")
#     bot.send_message(message.chat.id, f"Телефонный номер: {phone}")
#     bot.send_message(message.chat.id, "С вами свяжутся в ближайшее время. Чтобы создать новое обращение, нажмите /start.")
#     del user_data[message.chat.id]