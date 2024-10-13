import asyncio
import webbrowser
import time
import sqlite3

import telebot
from telebot import types

bot = telebot.TeleBot('7876492559:AAFBAv_CnHqcrdX-vGOD7aWZkJGqkpNlgus')


@bot.message_handler(commands=['start'])
def startBot(message):
    if message.from_user.last_name and message.from_user.first_name:
        first_mess = (f"Привет, <b>{message.from_user.first_name} {message.from_user.last_name}</b>.\n"
                      f"Хочешь ли ты зарегистрироваться?")
    else:
        first_mess = (f"Привет, <b>{message.from_user.first_name} </b>. \n"
                      f"Хочешь ли ты зарегистрироваться?")
    markup = types.InlineKeyboardMarkup()
    # button_creator = types.InlineKeyboardButton(text='Страница создателя', url='https://t.me/asmirzoian')
    # button2 = types.InlineKeyboardButton(text='Страница соседа', url='https://t.me/Al1tap')
    # markup.row(button_creator, button2)
    markup.row(types.InlineKeyboardButton(text='Да', callback_data='registration'),
               types.InlineKeyboardButton(text='Нет', callback_data='no'))
    markup.add(types.InlineKeyboardButton("Показать список пользователей", callback_data='show_users'))
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
        connection = sqlite3.connect('demobot.sql')
        cur = connection.cursor()

        cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, '
                    'name varchar(50), age int, password varchar(50))')
        connection.commit()

        cur.close()
        connection.close()

        bot.send_message(callback.message.chat.id, 'Введите свое имя:')
        bot.register_next_step_handler(callback.message, input_name)

    elif callback.data == 'show_users':
        connection = sqlite3.connect('demobot.sql')
        cur = connection.cursor()

        cur.execute('SELECT * FROM users')
        fetch = cur.fetchall()

        users = ''
        for el in fetch:
            users += (f'Имя: {el[1]}\n'
                      f'Возраст: {el[2]}\n'
                      f'Пароль: {el[3]}')

        cur.close()
        connection.close()

        bot.reply_to(callback.message, users)


def input_name(message):
    data = {
        'name': f"{message.text}",
        'age': '',
        'password': ''
    }
    bot.send_message(message.chat.id, 'Введите возраст:')
    bot.register_next_step_handler(message, input_age, data)


def input_age(message, data):
    data['age'] = message.text
    bot.send_message(message.chat.id, 'Введите пароль:')
    bot.register_next_step_handler(message, input_password, data)


def input_password(message, data):
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
            time.sleep(0.1)  # Добавим задержку, чтобы избежать ограничения по запросам
        except Exception as e:
            message_id -= 1


bot.infinity_polling()
