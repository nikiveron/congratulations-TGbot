from Person import Person
from ButtonsAndTexts import Texts
from ButtonsAndTexts import Buttons as Btn
import telebot
from telebot import types
import requests
import mylogger
import os
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv("bot_token")
bot = telebot.TeleBot(bot_token)
api_key = os.getenv("chat_token")
user_data = {}
mylogger.logfile_define()

def get_user_data(chat_id):
    if chat_id not in user_data:
        user_data[chat_id] = Person("None", 0, "None", "None", "None", "None", "None")
    return user_data[chat_id]

def get_congratulation(prompt):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral/ministral-8b",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 256,
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)
    try:
        response.raise_for_status()
        result = response.json()
        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        elif "error" in result:
            return f"Ошибка: {result['error']['message']}"
        else:
            return "Неожиданный ответ от API"
    except Exception as e:
        return f"Ошибка при запросе: {e}"

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Создать'))
    markup.add(types.KeyboardButton('О нас'))
    markup.add(types.KeyboardButton('Помощь'))
    bot.send_message(message.chat.id,
                     f"Привет, {message.from_user.first_name}! Я бот для создания поздравлений🎉\n\nДля того чтобы начать нажми на кнопку 'Создать'",
                     reply_markup=markup)

def on_click(message):
    if message.text == 'Создать':
        get_create(message)
    elif message.text == 'О нас':
        get_about(message)
    elif message.text == 'Помощь':
        get_help(message)

@bot.message_handler(commands=['help'])
def get_help(message):
    bot.send_message(message.chat.id, Texts.helpText)

@bot.message_handler(commands=['about'])
def get_about(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Мое CV:', url=Texts.cvURL))
    bot.send_message(message.chat.id, Texts.aboutText, reply_markup=markup)

@bot.message_handler(commands=['create'])
def get_create(message):
    person = get_user_data(message.chat.id)
    markup = types.InlineKeyboardMarkup()
    markup.row(*Btn.sexButtons)
    bot.send_message(message.chat.id,
                     '''\tДавай начнем создавать поздравление!\nКому ты хочешь записать поздравление?''',
                     reply_markup=markup)

def process_command_during_input(message):
    if message.text == '/start':
        start(message)
    elif message.text == '/help':
        get_help(message)
    elif message.text == '/about':
        get_about(message)
    elif message.text == '/create':
        get_create(message)
    else:
        bot.send_message(message.chat.id, "Неизвестная команда. Попробуй снова.")

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    person = get_user_data(callback.message.chat.id)

    # запись пола и определение имени
    if callback.data == 'get_create_f':
        person.sex = 'женщина'
        bot.send_message(callback.message.chat.id, "Отлично! Как зовут нашего получателя?")
        bot.register_next_step_handler_by_chat_id(callback.message.chat.id, lambda m: get_name(m, person))

    elif callback.data == 'get_create_m':
        person.sex = 'мужчина'
        bot.send_message(callback.message.chat.id, "Отлично! Как зовут нашего получателя?")
        bot.register_next_step_handler_by_chat_id(callback.message.chat.id, lambda m: get_name(m, person))

    # запись праздника определение стиля поздравления
    elif callback.data.startswith('holiday_'):
        if callback.data == 'holiday_pozh':
            person.holiday = 'простое пожелание'
        elif callback.data == 'holiday_hb':
            person.holiday = 'День Рождения'
        elif callback.data == 'holiday_ny':
            person.holiday = 'Новый Год'
        elif callback.data == 'holiday_23':
            person.holiday = '23 февраля'
        elif callback.data == 'holiday_8':
            person.holiday = '8 марта'
        elif callback.data == 'holiday_etc':
            bot.send_message(callback.message.chat.id, "Так... Отправь мне название праздника")
            bot.register_next_step_handler_by_chat_id(callback.message.chat.id, lambda m: get_holiday_etc(m, person))
            return

        markup = types.InlineKeyboardMarkup()
        markup.add(*Btn.styleButtons, row_width=1)
        bot.send_message(callback.message.chat.id, "✨ Супер! Давай выберем стиль поздравления:", reply_markup=markup)

    # запись стиля поздравления
    elif callback.data.startswith('style_'):
        if callback.data == 'style_of':
            person.style = 'официальный'
        elif callback.data == 'style_dr':
            person.style = 'дружеский'
        elif callback.data == 'style_ro':
            person.style = 'романтический'

        markup = types.InlineKeyboardMarkup()
        markup.add(*Btn.lengthButtons, row_width=1)
        bot.send_message(callback.message.chat.id, "💫 Класс! Выбери длину поздравления:", reply_markup=markup)

    elif callback.data.startswith('len_'):
        if callback.data == 'len_s':
            person.text_length = 'короткое, в одно предложение'
        elif callback.data == 'len_m':
            person.text_length = 'среднее, в несколько предложений'
        elif callback.data == 'len_l':
            person.text_length = 'длинное'
        create_exit(callback.message, person)

    elif callback.data == 'exit_y':
        bot.send_message(callback.message.chat.id, f"Готовим твое поздравление...⏳")
        mylogger.log_to_csv(person.name, person.age, person.sex, person.holiday, person.style, person.text_length)
        generate_congratulation(callback, person)

    elif callback.data == 'exit_n':
        bot.send_message(callback.message.chat.id, f"Ой... Давай попробуем еще раз! Нажми на кнопку 'Создать'")

    elif callback.data == 'generation':
        generate_congratulation(callback, person)

def get_name(message, person):
    if message.text.startswith('/'):
        process_command_during_input(message)
        return
    else:
        person.name = message.text
        if person.sex == "женщина":
            bot.send_message(message.chat.id, f'Хорошо!😁 Сколько ей лет? Напиши возраст числом!')
        else:
            bot.send_message(message.chat.id, f'Хорошо!😁 Сколько ему лет? Напиши возраст числом!')
        bot.register_next_step_handler_by_chat_id(message.chat.id, lambda m: get_age(m, person))

def get_age(message, person):
    if message.text.startswith('/'):
        process_command_during_input(message)
        return
    else:
        person.age = message.text
        if person.age.isdigit():
            if 0 < int(person.age) < 120:
                markup = types.InlineKeyboardMarkup()
                markup.add(*Btn.holidayButtons, row_width=1)
                bot.send_message(message.chat.id, f'А с каким праздником ты хочешь поздравить?', reply_markup=markup)
            else:
                bot.send_message(message.chat.id, f'Ты ввел некорректный возраст... Попробуй еще раз! Введи возраст числом')
                bot.register_next_step_handler_by_chat_id(message.chat.id, lambda m: get_age(m, person))
        else:
            bot.send_message(message.chat.id, f'Ты ввел некорректный возраст... Попробуй еще раз! Введи возраст числом')
            bot.register_next_step_handler_by_chat_id(message.chat.id, lambda m: get_age(m, person))

def get_holiday_etc(message, person):
    if message.text.startswith('/'):
        process_command_during_input(message)
        return
    else:
        person.holiday = message.text
        markup = types.InlineKeyboardMarkup()
        markup.row(*Btn.styleButtons)
        bot.send_message(message.chat.id, "✨ Супер! Давай выберем стиль поздравления:", reply_markup=markup)

def create_exit(message, person):
    markup = types.InlineKeyboardMarkup()
    markup.row(*Btn.ynButtons)
    bot.send_message(message.chat.id,
                     f"Супер! Все готово) Давай проверим данные!\n\nНаш получатель: \nимя: {person.name} \nпол: {person.sex} \nвозраст: {person.age} \nпраздник: {person.holiday} \nстиль поздравления: {person.style} \nдлина поздравления: {person.text_length} \n\nВсе верно?", reply_markup=markup)

def generate_congratulation(callback, person):
    prompt = f"Напиши {person.text_length} поздравление c праздником \"{person.holiday}\" для {'женщины' if person.sex == 'женщина' else 'мужчины'}, по имени {person.name}, возраст: {person.age}, поздравление должно быть в {person.style} стиле."
    markup = types.InlineKeyboardMarkup()
    new_generation_btn = types.InlineKeyboardButton('Перегенерировать🔄️', callback_data='generation')
    markup.add(new_generation_btn)

    congrat_text = get_congratulation(prompt)
    bot.send_message(callback.message.chat.id, f"{congrat_text}", reply_markup=markup)


@bot.message_handler()
def info(message):
    on_click(message)

bot.polling(none_stop=True, interval=0)
