import telebot
from telebot import types
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random
from gen import generator
from config import TOKEN
from loader import loader
import time
import yaml

questions = loader.load_questions()

bot = telebot.TeleBot(TOKEN)

current_question_index = -1
score = 0

waiting_for_first_value = False
waiting_for_second_value = False
waiting_for_action = False
is_quiz_active = False  # флаг для проверки активен ли квиз


facts = [
    "АВИСМА был основан в 1937 году как учебное заведение для подготовки специалистов в области авиации и спасательных работ.",
    "Основная цель института — обучение и подготовка специалистов в области гражданской авиации, авиационного спасения, и поисково-спасательных операций.",
    "В АВИСМА обучают по различным направлениям, включая пилотирование, эксплуатацию авиации, безопасность на воздушном транспорте и технику безопасности при аварийных ситуациях.",
    "Студенты АВИСМА проходят как теоретическую подготовку, так и практические тренировки на реальных авиационных тренажерах.",
    "Институт активно занимается научной работой в области авиационной безопасности, разработки новых технологий для спасательных операций и повышения эффективности поисково-спасательных работ.",
    "АВИСМА сотрудничает с международными учебными и научными организациями в области авиации, предоставляя своим студентам возможность обмена опытом с коллегами со всего мира.",
    "Студенты проходят стажировки и практику на реальных авиационных объектах, что помогает получить опыт в реальных условиях и подготовиться к работе в экстренных ситуациях.",
    "В рамках подготовки будущих специалистов, АВИСМА обучает действиям при пожарных авариях на воздушных судах, включая использование специализированного оборудования для тушения пожаров в воздухе.",
    "Студенты изучают технику и тактику спасательных операций, включая работу в экстремальных условиях и взаимодействие с другими спасательными службами.",
    "В числе заказчиков и партнеров АВИСМА — ведущие авиакомпании, государственные структуры и предприятия, работающие в сфере авиации и спасательных операций.",
    "Институт имеет современные тренажерные комплексы, авиационные симуляторы, а также площадки для практических занятий, имитирующие реальные аварийные ситуации.",
    "В последние годы институт также развивает программы для подготовки специалистов по спасению на воздушных судах, участвующих в космических миссиях и операциях по поиску и спасению в космосе.",
    "В рамках обучения большое внимание уделяется вопросам безопасности полетов, включая создание эффективных систем предотвращения аварий и инцидентов на борту воздушных судов."
]

def faq(file_path='data/data.yml'):
        random_id = random.randint(0, 4)
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        return data['questions'][random_id]

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    global is_quiz_active

    bot.reply_to(message, 'Добро пожаловать в чат-бот АВИСМА!')

    # создание клавиатуры
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Кто вы?', 'Прикольчики', 'FAQ')
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)

    is_quiz_active = False  # Убедитесь, что квиз не активен после отправки меню

@bot.message_handler(func=lambda message: message.text == 'Прикольчики')
def features(message):
    # Обновим, чтобы другие опции, такие как калькулятор или факты, работали
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Калькулятор', 'Факты', 'Квиз', 'Назад')
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == 'Квиз')
def start_quiz(message):
    global current_question_index, score, is_quiz_active
    score = 0
    current_question_index = -1
    is_quiz_active = True  # Устанавливаем флаг на True
    ask_next_question(message)

def ask_next_question(message):
    global is_quiz_active, score, current_question_index
    if not is_quiz_active:  # Если квиз не активен, не задаем вопросы
        return

    # Переход к следующему вопросу
    if current_question_index < len(questions) - 1:  # Убедитесь, что вопрос в пределах списка
        current_question_index += 1

    if current_question_index < len(questions):
        question = questions[current_question_index]

        if 'answers' not in question:
            print(f"Warning: Missing 'answers' for question {current_question_index + 1}")
            return

        answers = question['answers']

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for answer in answers:
            keyboard.add(answer)

        bot.send_message(
            message.chat.id, 
            f"Вопрос {current_question_index + 1}: {question['question']}",
            reply_markup=keyboard
        )
    else:
        # Завершаем квиз, если вопросов больше нет
        bot.send_message(message.chat.id, f"Квиз завершён! Ваш счёт: {score}/{len(questions)}")
        current_question_index = -1  # Сбросим индекс на -1
        score = 0  # Сбросим счёт
        is_quiz_active = False  # Сбрасываем флаг квиза

        # Возвращаем клавиатуру после завершения квиза
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('Кто вы?', 'Прикольчики', 'FAQ')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)

@bot.message_handler(func=lambda message: is_quiz_active)
def handle_quiz_answer(message):
    global current_question_index, score, is_quiz_active

    # Если текущий вопрос существует
    if current_question_index < len(questions):
        question = questions[current_question_index]
        correct_answer = question['correct_answer']

        # Проверяем, правильно ли ответил пользователь
        if message.text == correct_answer:
            score += 1
            bot.send_message(message.chat.id, "Правильно! 🎉")
        else:
            bot.send_message(message.chat.id, f"Неправильно! 😞 Правильный ответ: {correct_answer}")

        # Переход к следующему вопросу только после обработки ответа
        if current_question_index < len(questions) - 1:
            ask_next_question(message)  # Вопрос теперь задается в ask_next_question, а не здесь
        else:
            # Завершаем квиз после последнего вопроса
            bot.send_message(message.chat.id, f"Квиз завершён! Ваш счёт: {score}/{len(questions)}")
            current_question_index = -1  # Сбросим индекс на -1
            score = 0  # Сбросим счёт
            is_quiz_active = False  # Сбрасываем флаг квиза

            send_welcome()


@bot.message_handler(func=lambda message: message.text == 'Калькулятор')
def start_calculation(message):
    if not is_quiz_active:  # Проверяем, что квиз не активен
        global waiting_for_first_value
        waiting_for_first_value = True
        bot.send_message(message.chat.id, 'Введите первое значение:')

@bot.message_handler(func=lambda message: waiting_for_first_value)
def get_first_value(message):
    global first_value, waiting_for_first_value
    try:
        first_value = float(message.text)
        waiting_for_first_value = False
        global waiting_for_second_value
        waiting_for_second_value = True
        bot.send_message(message.chat.id, f'Первое значение: {first_value}. Теперь введите второе значение:')
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите корректное число для первого значения.')

@bot.message_handler(func=lambda message: waiting_for_second_value)
def get_second_value(message):
    global second_value, waiting_for_second_value
    try:
        second_value = float(message.text)
        waiting_for_second_value = False
        global waiting_for_action
        waiting_for_action = True

        # Кнопки для выбора действия
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('+', '-', '*', '/')
        bot.send_message(message.chat.id, f'Второе значение: {second_value}. Теперь выберите действие:', reply_markup=keyboard)
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите корректное число для второго значения.')

@bot.message_handler(func=lambda message: waiting_for_action)
def get_action(message):
    global action, waiting_for_action
    if message.text in ['+', '-', '*', '/']:
        action = message.text
        waiting_for_action = False
        calculate(message)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, выберите одно из доступных действий: +, -, * или /.')

def calculate(message):
    global first_value, second_value, action

    if action == '+':
        result = first_value + second_value
    elif action == '-':
        result = first_value - second_value
    elif action == '*':
        result = first_value * second_value
    elif action == '/':
        if second_value != 0:
            result = first_value / second_value
        else:
            bot.send_message(message.chat.id, 'Ошибка! На ноль делить нельзя.')
            return

    bot.send_message(message.chat.id, f'Результат: {result}')

    # После вычисления, бот предлагает начать новый расчет
    global waiting_for_first_value, waiting_for_second_value, waiting_for_action
    waiting_for_first_value = False
    waiting_for_second_value = False
    waiting_for_action = False

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Начать новый расчет', 'Назад')
    bot.send_message(message.chat.id, 'Хотите сделать еще один расчет?', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == 'Начать новый расчет')
def restart_calculation(message):
    global first_value, second_value, action
    first_value = None
    second_value = None
    action = None

    start_calculation(message)  # Снова начнем с первого значения

@bot.message_handler(func=lambda message: message.text == 'Факты')
def send_fact(message):
    if not is_quiz_active:  # Проверяем, что квиз не активен
        fact = random.choice(facts)
        if random.randint(1, 2) == 1:
            image_data = generator.create_fact_image(fact)
        else:
            image_data = generator.create_fact_image_static(fact)
        bot.send_photo(message.chat.id, image_data)

@bot.message_handler(func=lambda message: message.text == 'Назад')
def back(message):
    send_welcome(message)  # Возвращаемся в основное меню

# def handle_updates(updates):
#     for update in updates:
#         bot.process_new_updates([update])

# while True:
#     updates = bot.get_updates(offset=-1, limit=5, timeout=60)  # Get the latest updates
#     if updates:
#         handle_updates(updates)
#     time.sleep(1)  # Wait for a second before checking for new updates again

@bot.message_handler(func=lambda message: message.text == 'FAQ')
def faq(message):

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Интересный факт', 'Назад')
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == 'Интересный факт')
def send_fact(message):
    
    fact = load_random_fact()

    response = f'Вопрос: {fact['question']}\n\nОтвет: {fact['answer']}'
    bot.send_message(message.chat.id, response)

def load_random_fact():
    random_id = random.randint(0, 4)
    with open('data/data.yml', 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data['questions'][random_id]

bot.polling()