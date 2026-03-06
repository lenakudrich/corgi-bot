import telebot
import os
import time
from telebot import types

# Токен из переменных окружения
TOKEN = os.environ.get('TOKEN')
ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID')

if not TOKEN:
    raise ValueError("Нет токена! Добавь TOKEN в переменные окружения")

bot = telebot.TeleBot(TOKEN)

# Словарь для хранения состояния пользователя
user_state = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("🐶 Купить щенка")
    btn2 = types.KeyboardButton("👀 Посмотреть щенков")
    btn3 = types.KeyboardButton("📸 Фотосессия")
    btn4 = types.KeyboardButton("❓ Помощь")
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_message(
        message.chat.id,
        "👋 *Привет! Я бот питомника CorgiMax*\n\n"
        "Я помогу тебе:\n"
        "• Приобрести щенка корги\n"
        "• Записаться на фотосессию\n"
        "• Получить консультацию\n\n"
        "Выбери, что тебя интересует 👇",
        parse_mode='Markdown',
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text
    
    if text == "🐶 Купить щенка":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ Оставить заявку", callback_data="buy_puppy"))
        markup.add(types.InlineKeyboardButton("📋 Смотреть каталог", url="https://corgimax.ru/puppies"))
        
        bot.send_message(
            chat_id,
            "🐕 *Щенки корги*\n\n"
            "В данный момент у нас нет доступных щенков.\n"
            "Следующий помет скоро!\n"
            "Оставьте заявку, и мы сообщим вам первыми о рождении новых малышей!\n\n"
            "Хотите оставить заявку или посмотреть каталог?",
            parse_mode='Markdown',
            reply_markup=markup
        )
    
    elif text == "👀 Посмотреть щенков":
        bot.send_message(
            chat_id,
            "📸 *Фото наших щенков:*\n\n"
            "Смотрите в нашем сообществе VK 👇",
            parse_mode='Markdown'
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📷 Открыть VK", url="https://vk.com/izmaksimkovo"))

    
    elif text == "📸 Фотосессия":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ Записаться", callback_data="photo_session"))
        markup.add(types.InlineKeyboardButton("🎨 Примеры работ", url="https://corgimax.ru/photoshoot#portfolio"))
        
        bot.send_message(
            chat_id,
            "📸 *Фотосессии с корги*\n\n"
            "• Профессиональный фотограф\n"
            "• Помощь в подготовке питомца\n"
            "• Перенос при плохой погоде\n\n"
            "Хотите записаться?",
            parse_mode='Markdown',
            reply_markup=markup
        )
    
    elif text == "❓ Контакты":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📝 Записаться на консультацию", callback_data="consult"))
        
        bot.send_message(
            chat_id,
            "📧 *Связаться с нами:*\n\n"
            "Email: izmaximkovo@gmail.com\n\n"
            "Или оставьте заявку на консультацию 👇",
            parse_mode='Markdown',
            reply_markup=markup
        )
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("🐶 Купить щенка"), types.KeyboardButton("📸 Фотосессия"))
        markup.add(types.KeyboardButton("❓ Помощь"))
        
        bot.send_message(
            chat_id,
            "Я не совсем понял. Выберите пункт меню 👇",
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    
    if call.data == "buy_puppy":
        admin_msg = f"🐶 *Новая заявка на щенка!*\n\n"
        admin_msg += f"👤 Пользователь: @{call.from_user.username or 'нет username'}\n"
        admin_msg += f"🆔 ID: {call.from_user.id}\n"
        admin_msg += f"💬 Написать: t.me/{call.from_user.username or f'user?id={call.from_user.id}'}"
        
        bot.send_message(ADMIN_CHAT_ID, admin_msg, parse_mode='Markdown')
        
        bot.send_message(
            chat_id,
            "✅ *Спасибо!*\n\nМы свяжемся с вами в ближайшее время.\n\nА пока посмотрите наших щенков на сайте 👇",
            parse_mode='Markdown'
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📷 Перейти на сайт", url="https://corgimax.ru/puppies"))
        bot.send_message(chat_id, "Нажмите на кнопку:", reply_markup=markup)
    
    elif call.data == "photo_session":
        admin_msg = f"📸 *Новая заявка на фотосессию!*\n\n"
        admin_msg += f"👤 Пользователь: @{call.from_user.username or 'нет username'}\n"
        admin_msg += f"🆔 ID: {call.from_user.id}\n"
        admin_msg += f"💬 Написать: t.me/{call.from_user.username or f'user?id={call.from_user.id}'}"
        
        bot.send_message(ADMIN_CHAT_ID, admin_msg, parse_mode='Markdown')
        
        bot.send_message(
            chat_id,
            "✅ *Спасибо!*\n\nМы свяжемся с вами для согласования даты фотосессии.\n\nА пока посмотрите примеры работ 👇",
            parse_mode='Markdown'
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📸 Портфолио", url="https://corgimax.ru/photoshoot#portfolio"))
        bot.send_message(chat_id, "Нажмите на кнопку:", reply_markup=markup)

         elif call.data == "consult":
        admin_msg = f"📝 *Заявка на консультацию!*\n\n"
        admin_msg += f"👤 Пользователь: @{call.from_user.username or 'нет username'}\n"
        admin_msg += f"🆔 ID: {call.from_user.id}\n"
        admin_msg += f"💬 Написать: t.me/{call.from_user.username or f'user?id={call.from_user.id}'}"
        
        bot.send_message(ADMIN_CHAT_ID, admin_msg, parse_mode='Markdown')
        
        bot.send_message(
            chat_id,
            "✅ *Спасибо!*\n\nМы свяжемся с вами для консультации в ближайшее время.",
            parse_mode='Markdown'
        )

if __name__ == '__main__':
    print(f"✅ Бот запущен с токеном: {TOKEN[:10]}...")
    print(f"📢 Канал админа: {ADMIN_CHAT_ID}")
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"⚠️ Ошибка: {e}")
            time.sleep(5)