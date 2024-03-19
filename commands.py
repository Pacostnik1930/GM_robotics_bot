
from telebot import types


def start(message, bot):
    markup = types.InlineKeyboardMarkup()
    btn_3d_scan = types.InlineKeyboardButton('3D СКАНИРОВАНИЕ', callback_data='3d_scan_main_menu')
    markup.row(btn_3d_scan)
    btn_3d_model = types.InlineKeyboardButton('3D МОДЕЛИРОВАНИЕ', callback_data='3d_model_main_menu')
    btn_3d_print = types.InlineKeyboardButton('3D ПЕЧАТЬ', callback_data='3d_print_main_menu')
    markup.row(btn_3d_model, btn_3d_print)
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! \nВыберите интересующий Вас раздел 😃", reply_markup=markup, parse_mode='HTML')


