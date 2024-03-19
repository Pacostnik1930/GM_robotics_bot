from telebot import types

class UserState:
    def __init__(self):
        self.is_photo_received = False
        self.is_photos_received = 0
        self.description_received = False
        self.description = ""
        self.photo_id = None
        self.is_editing_text = False

# Словарь для хранения состояний пользователей
user_states = {}

def get_user_state(user_id):
    if user_id not in user_states:
        user_states[user_id] = UserState()
    return user_states[user_id]

def start(message, bot):
    markup = types.InlineKeyboardMarkup()
    btn_3d_scan = types.InlineKeyboardButton('3D СКАНИРОВАНИЕ', callback_data='3d_scan_main_menu')
    markup.row(btn_3d_scan)
    btn_3d_model = types.InlineKeyboardButton('3D МОДЕЛИРОВАНИЕ', callback_data='3d_model_main_menu')
    btn_3d_print = types.InlineKeyboardButton('3D ПЕЧАТЬ', callback_data='3d_print_main_menu')
    markup.row(btn_3d_model, btn_3d_print)
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! \nВыберите интересующий Вас раздел 😃", reply_markup=markup, parse_mode='HTML')


def handle_photo(message, bot):
    state = get_user_state(message.from_user.id)
    state.is_photo_received = True
    state.is_photos_received += 1
    if state.is_photos_received == 1:
        bot.send_message(message.chat.id, "Фотография получена! Комментарии к фото.")
        state.description_received = True
        state.photo_id = message.photo[-1].file_id
    else: send_buttons_after_delete(message,bot)

def send_buttons_after_delete(message, bot):
    state = get_user_state(message.from_user.id)
    if state.is_photo_received:
        keyboard = types.InlineKeyboardMarkup()
        delete_button = types.InlineKeyboardButton(text="Удалить фото", callback_data="delete_photo")
        edit_text_button = types.InlineKeyboardButton(text="Редактировать текст", callback_data="edit_text")
        confirm_button = types.InlineKeyboardButton(text="Подтвердить отправку", callback_data="confirm_send")
        keyboard.row(delete_button)
        keyboard.row(edit_text_button)
        keyboard.row(confirm_button)   
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)

        
    
def handle_description(message, bot):
    state = get_user_state(message.from_user.id)
    state.description = message.text
    state.description_received = False
    bot.send_message(message.chat.id, f"Описание фронт работ сохранено: {state.description1}")

    keyboard = types.InlineKeyboardMarkup()
    delete_button = types.InlineKeyboardButton(text="Удалить фото", callback_data="delete_photo")
    edit_text_button = types.InlineKeyboardButton(text="Редактировать текст", callback_data="edit_text")
    confirm_button = types.InlineKeyboardButton(text="Подтвердить отправку", callback_data="confirm_send")
    keyboard.row(delete_button)
    keyboard.row(edit_text_button)
    keyboard.row(confirm_button)
    bot.send_message(message.chat.id,"Выберите действие",reply_markup = keyboard)

  

    


def delete_photo(call, bot):
    state = get_user_state(call.from_user.id)
    try:
        if state.is_editing_text:
            bot.delete_message(call.message.chat.id)
        else: bot.delete_message(call.message.chat.id, call.message.message_id - 4)
    except Exception as e:
        print(f"Ошибка при удалении сообщения: {e}")
    bot.send_message(call.message.chat.id, "Файл удален, загрузите новый файл")
    state.is_photo_received = False
    

    

def edit_text(call, bot):
    state = get_user_state(call.from_user.id)
    state.is_editing_text = True
    bot.send_message(call.message.chat.id, "Введите новое описание фронт работ:")

def handle_messages(message, bot):
    state = get_user_state(message.from_user.id)
    
    if state.is_editing_text:
        state.description = message.text
        bot.send_message(message.chat.id, f"Описание отредактировано: {state.description}")
        state.is_editing_text = False  # Завершаем процесс редактирования           
        
        keyboard = types.InlineKeyboardMarkup()
        delete_button = types.InlineKeyboardButton(text="Удалить фото", callback_data="delete_photo")
        edit_text_button = types.InlineKeyboardButton(text="Редактировать текст", callback_data="edit_text")
        confirm_button = types.InlineKeyboardButton(text="Подтвердить отправку", callback_data="confirm_send")
        keyboard.row(delete_button)
        keyboard.row(edit_text_button)
        keyboard.row(confirm_button)
        bot.send_message(message.chat.id,"Выберите действие",reply_markup = keyboard)

def confirm_send(call, bot):
    state = get_user_state(call.from_user.id)
    bot.send_message(call.message.chat.id, "Данные успешно отправлены!")
    if state.photo_id:
        bot.send_photo(call.message.chat.id, state.photo_id, caption=state.description)  
        bot.answer_callback_query(call.id) 
        bot.send_message(call.message.chat.id, f"{call.message.from_user.first_name}Специалист свяжется с Вами в ближайшее время")
        bot.send_message(call.message.chat.id, "Для повторного обращения нажмите /start")
    reset_user_state(call,bot)

def reset_user_state(call, bot):
    user_id = call.from_user.id
    print(f"Сброс состояния для пользователя {call.from_user.id}")  # Добавляем логирование
    if user_id in user_states:
        del user_states[user_id]  # Удаляем состояние пользователя для сброса
    bot.answer_callback_query(call.id)
    # start(call.message, bot)  # Повторно вызываем стартовое сообщение


def model_main_menu(call, bot):
    user_state = get_user_state(call.from_user.id)
    user_state.is_photo_received = True  # Помечаем, что пользователь перешел в режим добавления фото
    bot.send_message(call.message.chat.id, "Пожалуйста, отправьте мне фото для 3D моделирования.")

def configure_model_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start_handler(message):
        user_id = message.from_user.id
        print(f"Команда /start получена от {user_id}")
        start(message, bot)

    @bot.message_handler(content_types=['photo'])
    def handle_photo_handler(message):
        handle_photo(message, bot)          
        

    @bot.callback_query_handler(func=lambda call: call.data == 'delete_photo')
    def delete_photo_handler(call):
        delete_photo(call, bot)

    @bot.callback_query_handler(func=lambda call: call.data == 'edit_text')
    def edit_text_handler(call):
        edit_text(call, bot)
        
    @bot.message_handler(func=lambda message: get_user_state(message.from_user.id).description_received)
    def handle_description_handler(message):
        handle_description(message, bot)

    @bot.message_handler(func=lambda message: get_user_state(message.from_user.id).is_editing_text)
    def handle_messages_handler(message):
        handle_messages(message, bot)

    @bot.callback_query_handler(func=lambda call: call.data == 'confirm_send')
    def confirm_send_handler(call):
        confirm_send(call, bot)

    
    @bot.callback_query_handler(func=lambda call: call.data in ['3d_scan_main_menu', '3d_model_main_menu', '3d_print_main_menu'])
    def model_main_menu_handler(call):
        if call.data == '3d_model_main_menu':
            model_main_menu(call, bot)
        # Здесь можно добавить дополнительные обработчики для других кнопок главного меню


    # Добавляем обработчик для сброса состояния 
    @bot.callback_query_handler(func=lambda call: call.data == 'start')
    def reset_user_state_handler(call):
        reset_user_state(call, bot)





    