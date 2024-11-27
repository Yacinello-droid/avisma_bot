import telebot
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Добро пожаловать в чат-бот АВИСМА! Выберите вашу категорию:')

    # создание клавиатуры
    
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Школьники', 'Студенты')
    bot.send_message(message.chat.id, 'Кто вы?', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == 'Школьники')
def school_info(message):

    # создание Inline клавиатуры

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('Сайт ВСМПО-АВИСМА', url='https://vsmpo.ru/'))
    bot.send_message(message.chat.id, 'Информация для школьников:', reply_markup=keyboard)

bot.polling()