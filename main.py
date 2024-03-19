import telebot
from print import handle_3d_print
from print import print_main_menu
from print import handle_no_3d_model
from print import configure_print_handlers
from model_main_menu import model_main_menu
from scan_main_menu import scan_main_menu
from scan_main_menu import configure_scan_handlers
from model_main_menu import configure_model_handlers
from telebot import types
# from print import configure_handlers

bot = telebot.TeleBot('7138089393:AAEoBSwwCzVYOaUDEQdv6Vv0ILiaR-LwZ5k')

# class UserState:
#     def __init__(self):
#         self.is_photo_received = False
#         self.photos_received = 0
#         self.description_received = False
#         self.description = ""
#         self.photo_id = None
#         self.is_editing_text = False

# # Словарь для хранения состояний пользователей
# user_states = {}

# def get_user_state(user_id):
#     if user_id not in user_states:
#         user_states[user_id] = UserState()
#     return user_states[user_id]

def main_menu(bot):
    scan_main_menu(bot)
    model_main_menu(bot)
    handle_3d_print(bot)
    handle_no_3d_model(bot)
    print_main_menu(bot)


@bot.callback_query_handler(func=lambda call: call.data in ['3d_scan_main_menu', '3d_model_main_menu', '3d_print_main_menu','has_3d_model', 'no_3d_model'])
def main_menu_handler(call):
    if call.data == '3d_scan_main_menu':
        scan_main_menu(call, bot)
    elif call.data == '3d_model_main_menu':
        model_main_menu(call,bot) 
    elif call.data == '3d_print_main_menu':
        handle_3d_print(call,bot)          
    elif call.data =='has_3d_model':
            print_main_menu(call,bot)
    elif call.data == 'no_3d_model':
            handle_no_3d_model(call,bot)  

    

configure_scan_handlers(bot)
configure_model_handlers(bot)
configure_print_handlers(bot)

# Запускаем бота
if __name__ == "__main__":
    
    bot.polling(none_stop=True)


