try:
    print('Start')
    import telebot
    from telebot import types
    from dotenv import load_dotenv
    from email.mime.application import MIMEApplication
    import os
    import platform
    import re
    import datetime
    import time
    import sys
    import smtplib
    import translating
    import google
    import scout
    from you_client import youcom


    email_flag = 0
    start_time = time.time()
    is_os_windows = platform.system() == 'Windows'
    if is_os_windows:
        dirname = os.path.dirname(sys.executable)  # для exe
    else:
        dirname = os.path.dirname(__file__)  # для проекта

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

    bot = telebot.TeleBot(YOUR_BOT_API_TOKEN)

    bot.chat_data = {}
    request_global = ''
    chat_id = ''

    def save_data(data):
        with open(f'{dirname}\\search_data.txt', 'a', encoding='utf-8') as f:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            f.write(f'{now}: {data}\n')

    def set_chat_id(message):
        global chat_id
        if chat_id == '':
            chat_id = message.chat.id

    def hide_buttons(message):
        hide_markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Wait ...", reply_markup=hide_markup)


    @bot.message_handler(commands=['start'])
    def restart_bot(message):
        set_chat_id(message)
        username = message.chat.username
        phone_number = message.contact.phone_number if message.contact else None
        bot.send_message(message.chat.id, 'Wait ...')
        send_mail(f'New User in My AI Search bot', f'Chat ID: {chat_id}\nUsername: {username}\nPhone number: {phone_number}')
        bot.delete_message(message.chat.id, message.message_id + 1)
        bot.send_message(message.chat.id, 'Please write your request:')


    @bot.message_handler(func=lambda message: True and message.text not in ['SCOU', 'YCOM', 'GOOG', 'TRAN', '.', '/', '-', '*', ',', 's::', 'c::', 'с::', 'y::', 'ю::', 'у::', 'g::', 'г::', 't::', 'т::', 'п::', ])
    def handle_message(message):
        request = message.text.lower()
        chars_to_check = ['s::', 'c::', 'с::', 'y::', 'ю::', 'у::', 'g::', 'г::', 't::', 'т::', 'п::', ]
        if not any(char in request for char in chars_to_check):
            button1 = types.KeyboardButton('TRAN')
            button2 = types.KeyboardButton('GOOG')
            button3 = types.KeyboardButton('YCOM')
            button4 = types.KeyboardButton('SCOU')
            keyboard = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
            keyboard.add(button1, button2, button3, button4)
            global request_global
            request_global = request
            bot.send_message(message.chat.id, 'Please select an option of search:', reply_markup=keyboard)
            return 1

        search_hub(message)


    def search_hub(message):
        bot.send_message(message.chat.id, 'Wait ...')
        request = message.text
        if any(s in request.lower() for s in ('s::', 'c::', 'с::')):
            answer = scout.search_scout(request)
            bot.delete_message(message.chat.id, message.message_id + 1)
            bot.send_message(message.chat.id, answer)
            print('sct')
            bot.send_message(message.chat.id, 'Please write your request:')
            set_chat_id(message)
            save_data(f'{chat_id} - {request}')

        elif any(s in request.lower() for s in ('y::', 'ю::', 'у::')):
            request_first = translating.translate_request(request)
            answer = youcom.ask(request_first)["response"]
            bot.delete_message(message.chat.id, message.message_id + 1)
            bot.send_message(message.chat.id, answer)
            bot.send_message(message.chat.id, 'Please write your request:')
            set_chat_id(message)
            save_data(f'{chat_id} - {request}')

        elif any(s in request.lower() for s in ('g::', 'г::')):
            answer = google.search_google(request)
            bot.delete_message(message.chat.id, message.message_id + 1)
            bot.send_message(message.chat.id, answer)
            bot.send_message(message.chat.id, 'Please write your request:')
            set_chat_id(message)
            save_data(f'{chat_id} - {request}')

        elif any(s in request.lower() for s in ('t::', 'т::', 'п::')):
            answer = translating.translate_request(request)
            bot.delete_message(message.chat.id, message.message_id + 1)
            bot.send_message(message.chat.id, answer)
            bot.send_message(message.chat.id, 'Please write your request:')
            set_chat_id(message)
            save_data(f'{chat_id} - {request}')


    @bot.message_handler(func=lambda message: message.text in ['SCOU', '.', '/', '-', '*', ',', 's::', 'c::', 'с::'])
    def show_text(message):
        hide_buttons(message)
        request = request_global.lower()
        answer = scout.search_scout(request)
        bot.delete_message(message.chat.id, message.message_id + 1)
        bot.send_message(message.chat.id, answer)
        bot.send_message(message.chat.id, 'Please write your request:')
        set_chat_id(message)
        save_data(f'{chat_id} - {request}')


    @bot.message_handler(func=lambda message: message.text in ['YCOM', 'y::', 'ю::', 'у::'])
    def show_text(message):
        hide_buttons(message)
        request_first = request_global.lower()
        request = translating.translate_request(request_first)
        answer = youcom.ask(request)["response"]
        bot.delete_message(message.chat.id, message.message_id + 1)
        bot.send_message(message.chat.id, answer)
        print('youcom')
        bot.send_message(message.chat.id, 'Please write your request:')
        set_chat_id(message)
        save_data(f'{chat_id} - {request_first}')


    @bot.message_handler(func=lambda message: message.text in ['GOOG', 'g::', 'г::'])
    def show_text(message):
        hide_buttons(message)
        request = request_global.lower()
        answer = google.search_google(request)
        bot.delete_message(message.chat.id, message.message_id + 1)
        bot.send_message(message.chat.id, answer)
        bot.send_message(message.chat.id, 'Please write your request:')
        set_chat_id(message)
        save_data(f'{chat_id} - {request}')


    @bot.message_handler(func=lambda message: message.text in ['TRAN', 't::', 'т::', 'п::'])
    def show_text(message):
        hide_buttons(message)
        request_first = request_global.lower()
        answer = translating.translate_request(request_first)
        bot.delete_message(message.chat.id, message.message_id + 1)
        bot.send_message(message.chat.id, answer)
        bot.send_message(message.chat.id, 'Please write your request:')
        set_chat_id(message)
        save_data(f'{chat_id} - {request_first}')


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

# try:
    bot.polling()
except Exception as e:
    error_message = f'Error: {e}'
    print(error_message)
    send_mail(f'ERROR in My AI Search bot', error_message)
finally:
    print('finally')
    # send_mail()
    bot.polling()

# pyinstaller --add-binary "D:\Dev\myseai\venv\Lib\site-packages\tls_client\dependencies\tls-client-64.dll;tls_client/dependencies" -F main.py
