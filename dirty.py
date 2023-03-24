import telebot
from telebot import types
from dotenv import load_dotenv
# import datetime as dt
import os
import platform
import re
import requests
import time
import smtplib
import scout
from you_client import youcom


email_flag = 0
start_time = time.time()
is_os_windows = platform.system() == 'Windows'

if is_os_windows:
    env_path = os.path.join('secrets.env')  # ◄local ▼
    load_dotenv(env_path)
    YOUR_BOT_API_TOKEN = os.getenv('YOUR_BOT_API_TOKEN')
    EMAIL_SENDER = os.getenv('EMAIL_SENDER')
    PASSWORD_EMAIL_SENDER = os.getenv('PASSWORD_EMAIL_SENDER')
    EMAIL_RECIEVER = os.getenv('EMAIL_RECIEVER')
else:
    YOUR_BOT_API_TOKEN = os.environ.get('YOUR_BOT_API_TOKEN')  # online ▼
    EMAIL_SENDER = os.environ.get('EMAIL_SENDER')
    PASSWORD_EMAIL_SENDER = os.environ.get('PASSWORD_EMAIL_SENDER')
    EMAIL_RECIEVER = os.environ.get('EMAIL_RECIEVER')


# Create a bot instance with your bot token
bot = telebot.TeleBot(YOUR_BOT_API_TOKEN)

# Create an empty dictionary to hold the chat data
bot.chat_data = {}
request_global = ''

def is_cyrillic(text):  # не работает
    cyrillic_pattern = re.compile('[а-яА-ЯёЁ]+')
    cyrillic_result = bool(cyrillic_pattern.fullmatch(text))
    return cyrillic_result

def is_unicode_escape(text):
    # Regular expression to match Unicode escape sequences
    unicode_escape_regex = re.compile(r"\\u[0-9a-fA-F]{4}")
    # Check if the string contains any Unicode escape sequences
    return unicode_escape_regex.search(text)

def hide_buttons(message):
    hide_markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Wait ...", reply_markup=hide_markup)

# Define a handler function to handle incoming messages
@bot.message_handler(commands=['start'])
def restart_bot(message):
    chat_id = message.chat.id
    username = message.chat.username
    phone_number = message.contact.phone_number if message.contact else None
    # send_mail(f'New User in My AI Search bot', f'Chat ID: {chat_id}\nUsername: {username}\nPhone number: {phone_number}')
    # # Save the user's message to the bot's memory
    # bot.chat_data.setdefault(message.chat.id, {})['message'] = message.text
    bot.send_message(message.chat.id, 'Please write your request:')

# Define a function to handle incoming messages
@bot.message_handler(func=lambda message: True and message.text != 'SCOUT' and message.text != 'YCOM (only English)')
def handle_message(message):
    request = message.text.lower()
    chars_to_check = ['s:', 'с:', 'c:', 'ц:', 'y:', 'у:', 'ю:']
    if not any(char in request for char in chars_to_check):
    # if 's:' not in request:
        # # message_text = message.text  # Remove the "/start " from the beginning of the message
        # bot.chat_data.setdefault(message.chat.id, {})['message'] = message.text
        button1 = types.KeyboardButton('SCOUT')
        button2 = types.KeyboardButton('YCOM (only English)')
        # Create the keyboard and add the buttons
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        keyboard.add(button1, button2)
        global request_global
        request_global = request
        # Send the message with the keyboard
        bot.send_message(message.chat.id, 'Please select an option of search:', reply_markup=keyboard)
        return 1

    # # Print the text of the incoming message
    # print(message.text)
    search_hub(message)

def search_hub(message):
    bot.send_message(message.chat.id, 'Wait ...')
    request = message.text
    if any(s in request.lower() for s in ('s:', 'c:', 'с:', 'ц:')):
        answer = scout.search_scout(request)
        bot.delete_message(message.chat.id, message.message_id + 1)
        bot.send_message(message.chat.id, answer)
        bot.send_message(message.chat.id, 'Please write your request:')

    elif any(s in request.lower() for s in ('y:', 'ю:', 'у:')):
        if is_cyrillic(request):
            bot.send_message(message.chat.id, 'Please rewrite your request in English or choose "SCOUT" button:')
            return 1
        answer = youcom.ask(request)["response"]
        bot.delete_message(message.chat.id, message.message_id + 1)
        bot.send_message(message.chat.id, answer)
        bot.send_message(message.chat.id, 'Please write your request:')

# Handler for the first button
@bot.message_handler(func=lambda message: message.text == 'SCOUT')
def show_text(message):
    hide_buttons(message)
    request = request_global.lower()
    answer = scout.search_scout(request)
    bot.delete_message(message.chat.id, message.message_id + 1)
    bot.send_message(message.chat.id, answer)
    bot.send_message(message.chat.id, 'Please write your request:')

# Handler for the first button
@bot.message_handler(func=lambda message: message.text == 'YCOM (only English)')
def show_text(message):
    hide_buttons(message)
    request = request_global.lower()
    if is_cyrillic(request):
        bot.send_message(request.chat.id, 'Please rewrite your request in English or choose "SCOUT" button:')
        return 1
    answer = youcom.ask(request)["response"]
    bot.delete_message(message.chat.id, message.message_id + 1)
    bot.send_message(message.chat.id, answer)
    bot.send_message(message.chat.id, 'Please write your request:')

def send_mail(
    subject,
    text
):
    try:
        message = 'Subject: {}\n\n{}'.format(subject, f'{text}')
        server = smtplib.SMTP_SSL('mail.inbox.lv', 465)
        server.login(EMAIL_SENDER, PASSWORD_EMAIL_SENDER)
        server.sendmail(EMAIL_SENDER, EMAIL_RECIEVER, message)
        server.quit()
    except Exception as e:
        if is_os_windows:
            print(f'Email did not send: {e}')
        server.sendmail(EMAIL_SENDER, EMAIL_RECIEVER, 'Subject: {}\n\n{}'.format('error', 'error'))
    finally:
        pass

# # Enable debug logging
# import logging
# logger = telebot.logger
# logger.setLevel(logging.DEBUG)

# Start the bot
bot.polling()
