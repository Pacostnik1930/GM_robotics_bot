import telebot
import sqlite3
from telebot import types
from registration import handle_registration,handle_authorization,handle_confirmation
from scanning import handle_scanning, handle_back_to_photo_scanning, handle_add_photo_scanning, handle_next_step_scanning, handle_confirm_send_scanning
from modeling import handle_modeling,handle_back_to_photo_modeling,handle_add_photo_modeling,handle_next_step_modeling,handle_confirm_send_modeling
from print import handle_3d_print,handle_no_3d_model,handle_has_3d_model,handle_back_to_file_printing,handle_add_file_printing,handle_next_step_printing,handle_confirm_send_printing
bot = telebot.TeleBot('7138089393:AAEoBSwwCzVYOaUDEQdv6Vv0ILiaR-LwZ5k')

user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):

    # referrer_id = message.text.split()[1] if len(message.text.split()) > 1 else None
    # if referrer_id:
    #     user_data[message.chat.id] = {'referrer_id': referrer_id}
    #     handle_scanning(message, bot)

    unique_id = message.text.split('GMroboticsBot')[1] if 'GMroboticsBot' in message.text else None
    if unique_id:
        conn = sqlite3.connect('gmbot.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM registration WHERE unique_link LIKE ?", (f"%{unique_id}%",))
        # user = cursor.fetchone()
        cursor.close()
        conn.close()
    #     if user:
    #         # Пользователь найден, выполните необходимые действия
    #         bot.send_message(message.chat.id, f"Добро пожаловать, {user[2]}!")
    #     else:
    #         bot.send_message(message.chat.id, "Недействительная ссылка.")
    # else:
    #     bot.send_message(message.chat.id, "Пожалуйста, перейдите по уникальной ссылке для регистрации.")

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    btn8 = types.InlineKeyboardButton('Мне нужна услуга', callback_data='need_service')
    btn9 = types.InlineKeyboardButton('Я оказываю услугу', callback_data='provide_a_service')
    keyboard.add(btn8, btn9)
    bot.send_message(message.chat.id, "Привет! Выберите раздел:", reply_markup=keyboard)
    
def provide_service(message,bot):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn_reg = types.InlineKeyboardButton('Авторизация по Telegram ID', callback_data='Авторизация')
    btn_back = types.InlineKeyboardButton('Назад', callback_data='Назад')
    keyboard.add(btn_reg, btn_back)
    bot.send_message(message.chat.id, "Нажмите на кнопку 'Авторизация по Telegram ID' для авторизации.", reply_markup=keyboard)

def need_service(message,bot):    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('3Д моделирование', callback_data='3Д моделирование')
    btn2 = types.InlineKeyboardButton('3Д сканирование', callback_data='3Д сканирование')
    btn3 = types.InlineKeyboardButton('3Д печать', callback_data='3Д печать')
    keyboard.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Привет! Выберите раздел:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'need_service')
def callback_need_service(call):
    need_service(call.message,bot)    

@bot.callback_query_handler(func=lambda call: call.data == 'provide_a_service')
def callback_provide_service(call):
    provide_service(call.message,bot)
    
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



@bot.callback_query_handler(func=lambda call: call.data == 'confirm_send_scanning')
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
    send_welcome(call.message)

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

bot.polling()