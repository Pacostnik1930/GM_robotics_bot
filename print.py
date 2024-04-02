import telebot
from telebot import types


bot = telebot.TeleBot('7138089393:AAEoBSwwCzVYOaUDEQdv6Vv0ILiaR-LwZ5k')

user_data = {}





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
    send_confirmation_printing(message, bot, documents, description)

def send_confirmation_printing(message,bot, documents, description):
    bot.send_message(message.chat.id, "Данные отправлены:")
    for documents in documents:
        bot.send_document(message.chat.id, documents)
    bot.send_message(message.chat.id, f"Фронт работ: {description}")
    bot.send_message(message.chat.id, "С вами свяжутся в ближайшее время. Чтобы создать новое обращение, нажмите /start.")
    del user_data[message.chat.id]  

    


# def delete_photo(call, bot):
#     state = get_user_state(call.from_user.id)
#     try:
#         if state.is_editing_text:
#             bot.delete_message(call.message.chat.id)
#         else: bot.delete_message(call.message.chat.id, call.message.message_id - 4)
#     except Exception as e:
#         print(f"Ошибка при удалении сообщения: {e}")
#     bot.send_message(call.message.chat.id, "Файл удален, загрузите новый файл")
#     state.is_photo_received = False
    

    

# def edit_text(call, bot):
#     state = get_user_state(call.from_user.id)
#     state.is_editing_text = True
#     bot.send_message(call.message.chat.id, "Введите новое описание фронт работ:")

# def handle_messages(message, bot):
#     state = get_user_state(message.from_user.id)
    
#     if state.is_editing_text:
#         state.description = message.text
#         bot.send_message(message.chat.id, f"Описание отредактировано: {state.description}")
#         state.is_editing_text = False  # Завершаем процесс редактирования           
        
#         keyboard = types.InlineKeyboardMarkup()
#         delete_button = types.InlineKeyboardButton(text="Удалить фото", callback_data="delete_photo")
#         edit_text_button = types.InlineKeyboardButton(text="Редактировать текст", callback_data="edit_text")
#         confirm_button = types.InlineKeyboardButton(text="Подтвердить отправку", callback_data="confirm_send")
#         keyboard.row(delete_button)
#         keyboard.row(edit_text_button)
#         keyboard.row(confirm_button)
#         bot.send_message(message.chat.id,"Выберите действие",reply_markup = keyboard)

# def confirm_send(call, bot):
#     state = get_user_state(call.from_user.id)
#     bot.send_message(call.message.chat.id, "Данные успешно отправлены!")
#     if state.photo_id:
#         bot.send_photo(call.message.chat.id, state.photo_id, caption=state.description)  
#         bot.answer_callback_query(call.id) 
#         bot.send_message(call.message.chat.id, f"{call.message.from_user.first_name}Специалист свяжется с Вами в ближайшее время")
#         bot.send_message(call.message.chat.id, "Для повторного обращения нажмите /start")
#     reset_user_state(call,bot)


        
# def reset_user_state(call, bot):
#     user_id = call.from_user.id
#     print(f"Сброс состояния для пользователя {call.from_user.id}")  # Добавляем логирование
#     if user_id in user_states:
#         del user_states[user_id]  # Удаляем состояние пользователя для сброса
#     bot.answer_callback_query(call.id)
#     # start(call.message, bot)  # Повторно вызываем стартовое сообщение




# def configure_print_handlers(bot):
#      @bot.message_handler(commands=['start'])
#      def start_handler(message):
#         user_id = message.from_user.id
#         print(f"Команда /start получена от {user_id}")
#         start(message, bot)

#      @bot.callback_query_handler(func=lambda call: call.data == '3d_print_main_menu')
#      def handle_3d_print_handler(call):
#         handle_3d_print(call,bot)
        

#      @bot.callback_query_handler(func=lambda call: call.data == 'no_3d_model')
#      def handle_no_3d_model_handler(call):
#         handle_no_3d_model(call,bot)
        

#      @bot.callback_query_handler(func=lambda call: call.data == 'back_to_main_menu')
#      def handle_back_to_main_menu_handler(call):
#         start(call.message, bot)

#      @bot.message_handler(content_types=['photo'])
#      def handle_photo_handler(message):
#         handle_photo(message, bot)          
        

#      @bot.callback_query_handler(func=lambda call: call.data == 'delete_photo')
#      def delete_photo_handler(call):
#         delete_photo(call, bot)

#      @bot.callback_query_handler(func=lambda call: call.data == 'edit_text')
#      def edit_text_handler(call):
#         edit_text(call, bot)
        
#      @bot.message_handler(func=lambda message: get_user_state(message.from_user.id).description_received)
#      def handle_description_handler(message):
#         handle_description(message, bot)

#      @bot.message_handler(func=lambda message: get_user_state(message.from_user.id).is_editing_text)
#      def handle_messages_handler(message):
#         handle_messages(message, bot)

#      @bot.callback_query_handler(func=lambda call: call.data == 'confirm_send')
#      def confirm_send_handler(call):
#         confirm_send(call, bot)


#      @bot.callback_query_handler(func=lambda call: call.data in ['3d_scan_main_menu', '3d_model_main_menu', '3d_print_main_menu'])
#      def print_main_menu_handler(call):
#         if call.data == '3d_print_main_menu':
#             print_main_menu(call, bot)   

    #  @bot.callback_query_handler(func=lambda call: call.data == 'start')
    #  def reset_user_state_handler(call):
    #     reset_user_state(call, bot)
    