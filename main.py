import telebot
import random
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cycler   
import numpy as np
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

plt.style.use('dark_background')

np.random.seed(random.randint(00000000, 99999999))

N = 10
data = (np.geomspace(1, 10, 100) + np.random.randn(N, 100)).T
cmap = plt.cm.coolwarm
mpl.rcParams['axes.prop_cycle'] = cycler(color=cmap(np.linspace(0, 1, N)))

fig, ax = plt.subplots()
lines = ax.plot(data)

plt.savefig('images/foo.png')


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

@bot.message_handler(func=lambda message: message.text == 'Студенты')
def students_info(message):

    # создание Inline клавиатуры

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('Сайт ВСПМО-АВИСМА', url='https://vsmpo.ru/'))
    #bot.send_message(message.chat.id, 'Информация для студентов:', reply_markup=keyboard)
    bot.send_photo(message.chat.id, photo=open('images/foo.png', 'br'), caption='Информация для студентов', reply_markup=keyboard)

bot.polling()