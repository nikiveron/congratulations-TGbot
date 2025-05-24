import telebot
from telebot import types

class Texts:
    # тексты
    helpText = '''Что умеет этот бот?\n\nЭтот бот умеет создавать поздравления для ваших друзей, родственников, коллег и других ваших знакомых!\n\nПросто нажми на кнопку \'Создать\' и создание твоего персонального поздравления сразу же начнется!'''
    cvURL = 'https://drive.google.com/drive/folders/18hc1De47e6wqoB-JRsEln-70_lE-Ubsx?usp=drive_link'
    aboutText = 'Я обычный бот в телеграмме, а мой создатель студентка СГУ факультета КНИИТ!\n***\nВопросы и предложения отправляйте по адресу: @ginsengstrip :))'

class Buttons:
    #кнопки
    __btn_female = types.InlineKeyboardButton('Женщина', callback_data='get_create_f')
    __btn_male = types.InlineKeyboardButton('Мужчина', callback_data='get_create_m')
    sexButtons = [__btn_female,  __btn_male]

    # __btn_pozh = types.InlineKeyboardButton('Простое пожелание 💫', callback_data='holiday_pozh')
    __btn_hb = types.InlineKeyboardButton('🍰 День Рождения', callback_data='holiday_hb')
    __btn_ny = types.InlineKeyboardButton('🎄 Новый Год', callback_data='holiday_ny')
    __btn_23 = types.InlineKeyboardButton('🪖 23 февраля', callback_data='holiday_23')
    __btn_8 = types.InlineKeyboardButton('🪷 8 марта', callback_data='holiday_8')
    __btn_etc = types.InlineKeyboardButton('🎈 Другой праздник', callback_data='holiday_etc')
    holidayButtons = [__btn_hb, __btn_ny, __btn_23, __btn_8, __btn_etc]

    __btn_of = types.InlineKeyboardButton('✒️ Официальный', callback_data='style_of')
    __btn_dr = types.InlineKeyboardButton('👍🏻 Дружеский', callback_data='style_dr')
    __btn_ro = types.InlineKeyboardButton('💘 Романтичекий', callback_data='style_ro')
    styleButtons = [__btn_of, __btn_dr, __btn_ro]

    __btn_yes = types.InlineKeyboardButton('Даа!', callback_data='exit_y')
    __btn_no = types.InlineKeyboardButton('Нет((', callback_data='exit_n')
    ynButtons = [__btn_yes, __btn_no]

    __btn_short = types.InlineKeyboardButton('Короткое - одно предложение', callback_data='len_s')
    __btn_middle = types.InlineKeyboardButton('Среднее - несколько предложений', callback_data='len_m')
    __btn_long = types.InlineKeyboardButton('Длинное', callback_data='len_l')
    lengthButtons = [__btn_short, __btn_middle, __btn_long]