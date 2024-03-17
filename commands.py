import telebot
from telebot import types
import scan_main_menu


bot = telebot.TeleBot('7138089393:AAEoBSwwCzVYOaUDEQdv6Vv0ILiaR-LwZ5k')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn_3d_scan = types.InlineKeyboardButton('3D CКАНИРОВАНИЕ',callback_data='3d_scan_main_menu')
    markup.row(btn_3d_scan)
    btn_3d_model = types.InlineKeyboardButton('3D МОДЕЛИРОВАНИЕ',callback_data='3d_model_main_menu')
    btn_3d_print = types.InlineKeyboardButton('3D ПЕЧАТЬ',callback_data='3d_print_main_menu')
    markup.row(btn_3d_model,btn_3d_print)
    bot.send_message(message.chat.id,f"Привет,{message.from_user.first_name} ! \nВыберите интересующий Вас раздел \U0001F609",reply_markup=markup,parse_mode='HTML')
