import telebot

MyFirstBot = telebot.TeleBot('7876492559:AAFBAv_CnHqcrdX-vGOD7aWZkJGqkpNlgus')

from telebot import types


@MyFirstBot.message_handler(commands=['start'])
def startBot(message):
    if message.from_user.last_name and message.from_user.first_name:
        first_mess = f"Привет, <b>{message.from_user.first_name} {message.from_user.last_name}</b>, это мой первый бот для телеграма"
    else:
        first_mess = f"Привет, <b>{message.from_user.first_name} </b>, это мой первый бот для телеграма"
    markup = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton(text='Страница создателя', callback_data='Creator_url', url='https://t.me/asmirzoian')
    button_no = types.InlineKeyboardButton(text='Страница педика', callback_data='Gay_url', url='https://t.me/Al1tap')
    markup.add(button_yes)
    markup.add(button_no)
    MyFirstBot.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)


@MyFirstBot.callback_query_handler(func=lambda call:True)
def response(function_call):
  if function_call.message:
     if function_call.data == "1":
        second_mess = ""
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Перейти на сайт", url="https://timeweb.cloud/"))
        MyFirstBot.send_message(function_call.message.chat.id, second_mess, reply_markup=markup)
        MyFirstBot.answer_callback_query(function_call.id)
    # if function_call.data == "Gay_url":


MyFirstBot.infinity_polling()
