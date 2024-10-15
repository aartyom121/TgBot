import asyncio
import json
import webbrowser
import time
import sqlite3
import requests

import telebot
from telebot import types

bot = telebot.TeleBot('7876492559:AAFBAv_CnHqcrdX-vGOD7aWZkJGqkpNlgus')
API = '5650a3e59285de09b3c4ccf8919234d0'


@bot.message_handler(commands=['start'])
def startBot(message):
    if message.from_user.last_name and message.from_user.first_name:
        first_mess = (f"Привет, <b>{message.from_user.first_name} {message.from_user.last_name}</b>.\n"
                      f"Это мой тестовый телеграм бот")
    else:
        first_mess = (f"Привет, <b>{message.from_user.first_name} </b>. \n"
                      f"Это мой тестовый телеграм бот")
    markup = types.InlineKeyboardMarkup()
    # button_creator = types.InlineKeyboardButton(text='Страница создателя', url='https://t.me/asmirzoian')
    # button2 = types.InlineKeyboardButton(text='Страница соседа', url='https://t.me/Al1tap')
    # markup.row(button_creator, button2)
    markup.row(types.InlineKeyboardButton(text='Регистрация', callback_data='registration'),
               types.InlineKeyboardButton("Узнать погоду", callback_data='weather'))
    markup.row(types.InlineKeyboardButton("Показать список пользователей", callback_data='show_users'),
               types.InlineKeyboardButton(text='Очистить чат', callback_data='clean'))
    bot.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['site', 'website'])
def site(message):
    bot.send_message(message.chat.id, f'<b>Открываю сайт!</b>', parse_mode='html')
    webbrowser.open("https://youtube.com")


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    delete_photo = types.InlineKeyboardButton(text='Удалить фото', callback_data='delete')
    edit_text = types.InlineKeyboardButton(text='Изменить фото', callback_data='edit')
    clean = types.InlineKeyboardButton(text='Очистить чат', callback_data='clean')
    markup.row(edit_text, delete_photo)
    markup.row(clean)
    bot.reply_to(message, 'Красивое фото!', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def photo_callback(callback):
    chat_id = callback.message.chat.id
    if callback.data == 'delete':
        bot.delete_message(chat_id, callback.message.message_id - 1)

    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', chat_id, callback.message.message_id)

    elif callback.data == 'clean':
        clean_chat(chat_id, callback.message.message_id)

    elif callback.data == 'registration':
        bot.delete_message(chat_id, callback.message.message_id)
        connection = sqlite3.connect('demobot.sql')
        cur = connection.cursor()

        cur.execute('CREATE TABLE IF NOT EXISTS users (id integer primary key autoincrement, '
                    'name varchar(50), age int, password varchar(50))')
        connection.commit()

        cur.close()
        connection.close()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton("Отмена"))

        bot.send_message(chat_id, 'Введите свое имя:', reply_markup=markup)
        bot.register_next_step_handler(callback.message, input_name)

    elif callback.data == 'show_users':
        if callback.message.text.startswith("Привет"):
            bot.delete_message(chat_id, callback.message.message_id)
        connection = sqlite3.connect('demobot.sql')
        cur = connection.cursor()

        cur.execute('SELECT * FROM users')
        fetch = cur.fetchall()

        users = ''
        i = 1
        for el in fetch:
            users += (f'{i}) Имя: {el[1]}\n'
                      f'Возраст: {el[2]}\n'
                      f'Пароль: {el[3]}\n\n')
            i += 1

        cur.close()
        connection.close()

        bot.send_message(chat_id, f'Список пользователей:\n{users}')

    elif callback.data == 'no':
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("Узнать погоду", callback_data='weather'))
        bot.send_message(chat_id, "Могу предложить вам узнать погоду", reply_markup=markup)

    elif callback.data == 'weather':
        bot.send_message(chat_id, "Введите название города")
        bot.register_next_step_handler(callback.message, get_weather)
    elif callback.data == 'start':
        startBot(callback.message)


def get_weather(message):
    city = message.text.lower()
    try:
        data_json = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}"
                                 f"&appid={API}&units=metric&lang=ru")
        data = json.loads(data_json.text)

        bot.reply_to(message, f"Температура: {int(data['main']['temp'])}°С\n"
                              f"Ощущается как: {int(data['main']['feels_like'])}°С\n"
                              f"Влажность: {data['main']['humidity']}%\n"
                              f"Описание: {data['weather'][0]['description']}", )
        startBot(message)

    except Exception:
        bot.reply_to(message, f'Ошибка.\nПожалуйста, повторите позже.')
        startBot(message)


def input_name(message):
    if message.text.lower() == "отмена":
        startBot(message)
        return
    data = {
        'name': f"{message.text}",
        'age': '',
        'password': ''
    }
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("Отмена"))
    bot.send_message(message.chat.id, 'Введите возраст:', reply_markup=markup)
    bot.register_next_step_handler(message, input_age, data)


def input_age(message, data):
    if message.text.lower() == "отмена":
        startBot(message)
        return
    data['age'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("Отмена"))
    bot.send_message(message.chat.id, 'Введите пароль:', reply_markup=markup)
    bot.register_next_step_handler(message, input_password, data)


def input_password(message, data):
    if message.text.lower() == "отмена":
        startBot(message)
        return
    data['password'] = message.text
    name = data['name']
    age = data['age']
    password = data['password']

    connection = sqlite3.connect('demobot.sql')
    cur = connection.cursor()

    cur.execute(f'INSERT INTO users (name, age, password) VALUES ("{name}", "{age}", "{password}")')
    connection.commit()

    cur.close()
    connection.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Показать список пользователей", callback_data='show_users'))
    bot.send_message(message.chat.id, "Успешная регистрация!", reply_markup=markup)


def clean_chat(chat_id, message_id):
    while message_id > 0:
        try:
            bot.delete_message(chat_id, message_id)
            message_id -= 1
            time.sleep(0.001)  # Добавим задержку, чтобы избежать ограничения по запросам
        except Exception as e:
            message_id -= 1


bot.infinity_polling()
