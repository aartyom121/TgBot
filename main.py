import webbrowser

import telebot

bot = telebot.TeleBot('7876492559:AAFBAv_CnHqcrdX-vGOD7aWZkJGqkpNlgus')

from telebot import types


@bot.message_handler()
def lox(message):
    while 1:
        bot.send_message(message.chat.id, 'ты пидор!')


@bot.message_handler(commands=['start'])
def startBot(message):
    if message.from_user.last_name and message.from_user.first_name:
        first_mess = f"Привет, <b>{message.from_user.first_name} {message.from_user.last_name}</b>, это мой первый бот для телеграма"
    else:
        first_mess = f"Привет, <b>{message.from_user.first_name} </b>, это мой первый бот для телеграма"
    markup = types.InlineKeyboardMarkup()
    button_creator = types.InlineKeyboardButton(text='Страница создателя', callback_data='Creator_url',
                                            url='https://t.me/asmirzoian')
    # button_gay = types.InlineKeyboardButton(text='Страница педика', callback_data='Gay_url', url='https://t.me/Al1tap')
    markup.add(button_creator)
    markup.add(types.InlineKeyboardButton(text='Страница педика', callback_data='Gay_url', url='https://t.me/Al1tap'))
    bot.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['site', 'website'])
def site(message):
    bot.send_message(message.chat.id, f'<b>Открываю сайт!</b>', parse_mode='html')
    webbrowser.open("https://youtube.com")


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    bot.reply_to(message, 'Какой ужас')


bot.infinity_polling()
