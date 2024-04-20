import config
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from random import randint
import sqlite3 

bot = telebot.TeleBot(config.API_TOKEN)

def senf_info(bot, message, row):
        
        info = f"""
📍Track name:   {row[2]}
📍Artist:                   {row[1]}
📍Release:                   {row[3]}
📍Genres:              {row[4]}
📍Topic:      {row[29]}
"""
        bot.send_message(message.chat.id, info, reply_markup=add_to_favorite(row[0]))


def add_to_favorite(id):
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(InlineKeyboardButton("Добавить фильм в избранное 🌟", callback_data=f'favorite_{id}'))
        return markup


def main_markup():
  markup = ReplyKeyboardMarkup()
  markup.add(KeyboardButton('/random'))
  return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith("favorite"):
        id = call.data[call.data.find("_")+1:]


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """Hello! You're welcome to the best Song-Chat-Bot!🎧
Here you can find 1000 songs 🔥
Click /random to get random song
Or write the name of song and I will try to find it! 🪩	""", reply_markup=main_markup())

@bot.message_handler(commands=['random'])
def random_movie(message):
    con = sqlite3.connect("data.db")
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM data ORDER BY RANDOM() LIMIT 1")
        row = cur.fetchall()[0]
        cur.close()
    senf_info(bot, message, row)

    
@bot.message_handler(func=lambda message: True)
def echo_message(message):

    con = sqlite3.connect("data.db")
    with con:
        cur = con.cursor()
        cur.execute(f"select * from data where LOWER(track_name) = '{message.text.lower()}'")
        row = cur.fetchall()
        if row:
            row = row[0]
            bot.send_message(message.chat.id,"Of course! I know this song😌")
            senf_info(bot, message, row)
        else:
            bot.send_message(message.chat.id,"I don't know this song ")

        cur.close()



bot.infinity_polling()