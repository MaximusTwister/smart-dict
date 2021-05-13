from telebot import TeleBot
from sys import modules

bot_token = '1768034163:AAFPzXAArraniiwGmTZZU9TrNxv0bIWr2Wc'
print(f'[{modules[__name__].__name__}] Creating Bot Instance')
bot = TeleBot(bot_token)
print(f'[{modules[__name__].__name__}] Bot: {bot}\n')