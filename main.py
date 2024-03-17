import telebot
from scan_main_menu import configure_handlers

bot = telebot.TeleBot('7138089393:AAEoBSwwCzVYOaUDEQdv6Vv0ILiaR-LwZ5k')

configure_handlers(bot)

# Запускаем бота
if __name__ == "__main__":
    bot.polling(none_stop=True)


