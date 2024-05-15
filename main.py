
import telebot
import sqlite3
from telebot import types
from registration import handle_registration,handle_authorization,handle_confirmation
from scanning import handle_scanning, handle_back_to_photo_scanning, handle_add_photo_scanning, handle_next_step_scanning, handle_confirm_send_scanning#, handle_name_scanning
from modeling import handle_modeling,handle_back_to_photo_modeling,handle_add_photo_modeling,handle_next_step_modeling,handle_confirm_send_modeling
from print import handle_3d_print,handle_no_3d_model,handle_has_3d_model,handle_back_to_file_printing,handle_add_file_printing,handle_next_step_printing,handle_confirm_send_printing
import _globals
import mysql.connector

bot = telebot.TeleBot('7138089393:AAEoBSwwCzVYOaUDEQdv6Vv0ILiaR-LwZ5k')

user_data = {}

@bot.message_handler(commands=['info'])
def information(message):
    bot.send_message(message.chat.id, "Здесь будет описание работы с ботом")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1930",
        database="gm_robotics"
    )
    cursor = conn.cursor()
    args = message.text.split()
    if len(args) == 1:
        handle_registration(message, bot)
    elif len(args) > 1:
        unique_id = args[1]
        print("unique_id=", unique_id)  # Вывод значения unique_id для проверки
        querry = "SELECT chat_id FROM registration WHERE unique_id = %s"
        values = ("https://t.me/GMroboticsBot?start=" + unique_id,)
        cursor.execute(querry,values)
        result = cursor.fetchone()
        print("sw: chat_id=", result[0], " for unique_id= ", unique_id)
        cursor.close()
        conn.close()
        
        if result:
            chat_id = result[0]
            if message.chat.id in user_data and user_data[message.chat.id]['unique_id'] == unique_id:
                # Пользователь уже переходил по этой ссылке, оставляем его внутри текущей ссылки
                _globals.gchat_id = chat_id
                print("sw: _globals.gchat_id=", _globals.gchat_id)
                bot.send_message(message.chat.id, f"Вы уже находитесь внутри ссылки от пользователя с ID: {chat_id}")
            else:
                # Пользователь переходит по новой ссылке
                _globals.gchat_id = chat_id
                print("sw: _globals.gchat_id=", _globals.gchat_id)
                bot.send_message(message.chat.id, f"Вы перешли по ссылке от пользователя с ID: {chat_id}")
                user_data[message.chat.id] = {'unique_id': unique_id}
        else:
            bot.send_message(message.chat.id, "Неверная ссылка.")



    keyboard = types.InlineKeyboardMarkup(row_width=2)
    btn8 = types.InlineKeyboardButton('Мне нужна услуга', callback_data='need_service')
    btn9 = types.InlineKeyboardButton('Я оказываю услугу', callback_data='provide_a_service')
    btn_info = types.InlineKeyboardButton('Инструкция по использованию',callback_data='get_info')
    keyboard.add(btn8, btn9,btn_info)
    bot.send_message(message.chat.id, "Выберите раздел:", reply_markup=keyboard)
    
def provide_service(message,bot):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn_reg = types.InlineKeyboardButton('Авторизация по Telegram ID', callback_data='Авторизация')
    btn_back = types.InlineKeyboardButton('Назад', callback_data='btn_back_reg')
    keyboard.add(btn_reg, btn_back)
    bot.send_message(message.chat.id, "Нажмите на кнопку 'Авторизация по Telegram ID' для авторизации.", reply_markup=keyboard)

def need_service(message,bot):    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('3Д моделирование', callback_data='3Д моделирование')
    btn2 = types.InlineKeyboardButton('3Д сканирование', callback_data='3Д сканирование')
    btn3 = types.InlineKeyboardButton('3Д печать', callback_data='3Д печать')
    keyboard.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Выберите раздел:", reply_markup=keyboard)

def get_info(message,bot):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn_back_info = types.InlineKeyboardButton('Назад',callback_data='back_info')
    keyboard.add(btn_back_info)
    info_text =  "\u0031\u20E3  Регистрация и получение уникальной ссылки:\n\
    - При регистрации Вы получаете уникальную ссылку, которая становится Вашим личным помощником.\n\n\
\u0032\u20E3 Размещение ссылки:\n\
    - Разместите эту ссылку на ресурсах, где Вы размещаете рекламу.\n\
    - Пользователь, перешедший по этой ссылке, попадает на Вашу страницу.\n\n\
\u0033\u20E3 Заполнение заявки:\n\
    - Когда пользователь заполняет заявку на Вашей странице, она автоматически поступает к Вам.\n\
    - Таким образом, Вы экономите время на сборе информации.\n\n\
\u0034\u20E3 Удобство хранения данных:\n\
    - Технические задания, фотографии и файлы приходят Вам на одну платформу для удобного доступа.\n\n\
\u0035\u20E3. Пример действия:\n\
    - Нажмите на кнопку 'Мне нужна услуга' для просмотра визуального примера работы бота."
    bot.send_message(message.chat.id,info_text,reply_markup=keyboard)  

@bot.callback_query_handler(func=lambda call: call.data == 'need_service')
def callback_need_service(call):
    need_service(call.message,bot)    

@bot.callback_query_handler(func=lambda call: call.data == 'provide_a_service')
def callback_provide_service(call):
    provide_service(call.message,bot)

@bot.callback_query_handler(func=lambda call: call.data == 'get_info')
def callback_get_info(call):
    get_info(call.message,bot)

@bot.callback_query_handler(func=lambda call: call.data == 'back_info')
def callback_back_info(call):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    btn8 = types.InlineKeyboardButton('Мне нужна услуга', callback_data='need_service')
    btn9 = types.InlineKeyboardButton('Я оказываю услугу', callback_data='provide_a_service')
    btn_info = types.InlineKeyboardButton('Инструкция по использованию',callback_data='get_info')
    keyboard.add(btn8, btn9,btn_info)
    bot.send_message(call.message.chat.id, "Привет! Выберите раздел:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'btn_back_reg')
def callback_btn_back_reg(call):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    btn8 = types.InlineKeyboardButton('Мне нужна услуга', callback_data='need_service')
    btn9 = types.InlineKeyboardButton('Я оказываю услугу', callback_data='provide_a_service')
    btn_info = types.InlineKeyboardButton('Инструкция по использованию',callback_data='get_info')
    keyboard.add(btn8, btn9,btn_info)
    bot.send_message(call.message.chat.id, "Привет! Выберите раздел:", reply_markup=keyboard)
    
@bot.callback_query_handler(func=lambda call: call.data == '3Д сканирование')
def scanning(call):
    handle_scanning(call.message, bot) 


@bot.callback_query_handler(func=lambda call: call.data == 'back_to_photo_scanning')
def callback_back_to_photo_scanning(call):
    handle_back_to_photo_scanning(call, bot)

@bot.callback_query_handler(func=lambda call: call.data == 'add_photo_scanning')
def callback_add_photo_scanning(call):
    handle_add_photo_scanning(call, bot)

@bot.callback_query_handler(func=lambda call: call.data == 'next_step_scanning')
def callback_next_step_scanning(call):
    handle_next_step_scanning(call, bot)


@bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_send_scanning_'))
def callback_confirm_send_scanning(call):
    handle_confirm_send_scanning(call)


@bot.callback_query_handler(func=lambda call: call.data == '3Д моделирование')
def modeling(call):
    handle_modeling(call.message, bot)

@bot.callback_query_handler(func=lambda call: call.data == 'back_to_photo_modeling')
def callback_back_to_photo_modeling(call):
    handle_back_to_photo_modeling(call, bot)

@bot.callback_query_handler(func=lambda call: call.data == 'add_photo_modeling')
def callback_add_photo_modeling(call):
    handle_add_photo_modeling(call, bot)        

@bot.callback_query_handler(func=lambda call: call.data == 'next_step_modeling')
def callback_next_step_modeling(call):
    handle_next_step_modeling(call, bot)  

@bot.callback_query_handler(func=lambda call: call.data == 'confirm_send_modeling')
def callback_confirm_send_modeling(call):
    handle_confirm_send_modeling(call)

@bot.callback_query_handler(func=lambda call: call.data == '3Д печать')
def printing(call):
    handle_3d_print(call.message,bot)

@bot.callback_query_handler(func=lambda call: call.data == 'no_3d_model')
def callback_no_3d_model(call):
    handle_no_3d_model(call, bot)    

@bot.callback_query_handler(func=lambda call: call.data == 'back_to_main_menu')
def calback_back_to_main_menu(call):
    message = call.message
    message.text = "/start"  # Устанавливаем текст сообщения в "/start"
    send_welcome(message)

@bot.callback_query_handler(func=lambda call: call.data == 'has_3d_model')
def callback_has_3d_model(call):
    handle_has_3d_model(call.message,bot)

@bot.callback_query_handler(func=lambda call: call.data == 'back_to_file_printing')
def callback_back_to_file_printing(call):
    handle_back_to_file_printing(call, bot)

@bot.callback_query_handler(func=lambda call: call.data == 'add_file_printing')
def callback_add_file_printing(call):
    handle_add_file_printing(call, bot)

@bot.callback_query_handler(func=lambda call: call.data == 'next_step_printing')
def callback_next_step_printing(call):
    handle_next_step_printing(call, bot) 

@bot.callback_query_handler(func=lambda call: call.data == 'confirm_send_printing')
def callback_confirm_send_printing(call):
    handle_confirm_send_printing(call)  

@bot.callback_query_handler(func=lambda call: call.data == 'Регистрация')           
def callback_registration(call):
    handle_registration(call.message,bot)

@bot.callback_query_handler(func=lambda call: call.data == 'Авторизация')    
def callback_authorization(call):
    handle_authorization(call.message,bot)

@bot.callback_query_handler(func=lambda call: call.data.startswith('Подтвердить_'))
def callback_confirmation(call):
    handle_confirmation(call,bot)

bot.polling(none_stop=True)
