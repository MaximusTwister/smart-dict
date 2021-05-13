from requests import exceptions

from bot_settings import bot
from django_connect import create_request


@bot.message_handler(func=lambda msg: msg.text.isalpha())
def new_word_handler(msg):
    print(f'Have a new message {msg}')
    msg_list = msg.text.split()
    if len(msg_list) > 1:
        word_phrase = 'phrase'
    else:
        word_phrase = 'word'

    if create_request(msg.text) is True:
        text_to_reply = f'Your {word_phrase} was send to __SmartDictionary__'
    else:
        text_to_reply = f'Sorry, I can not handle your request right now.\nTake another try in a while.'

    bot.reply_to(msg, text_to_reply)


if __name__ == '__main__':
    try:
        print('Telegram Bot is starting')
        bot.polling()
    except exceptions.ConnectionError as e:
        print('Network Issues with Telegram')
