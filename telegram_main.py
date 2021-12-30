import sqlite3
import telebot
from main import *

bot = telebot.TeleBot("5099099475:AAHNWwVNOoPR6oPELEntSy3UMlv8y2EZTTI", parse_mode='HTML')
conn = sqlite3.connect('db', check_same_thread=False)
cursor = conn.cursor()
user = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Добро пожаловать')


@bot.message_handler(commands=['settings'])
def start_message(message):
    msg = bot.send_message(message.chat.id, 'Введите логин')
    bot.register_next_step_handler(msg, get_login)

def get_login(message):
    user['username'] = message.text
    msg1 = bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(msg1, get_password)

def get_password(message):
    user['password'] = message.text
    add_user_to_db(message.from_user.id, ''+user['username'], user['password'])

def add_user_to_db(user_id: int, username: str, password: str):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (user_id, username, password) VALUES (?, ?, ?)',
                   (user_id, username, password))
    conn.commit()
@bot.message_handler(commands=['marks'])
def start_message(message):
    cursor = conn.cursor()
    cursor.execute('SELECT username, password FROM users WHERE user_id = ?', (message.from_user.id, ))
    rows = cursor.fetchall()
    username, password = '',''
    for row in rows:
        username, password = row[0], row[1]
    bot.send_message(message.chat.id, f'<pre>{get_table(parse_subjects(login(username=username, password=password)))}</pre>')
    
bot.polling(none_stop=True, interval=0)
