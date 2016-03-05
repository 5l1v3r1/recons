from .settings import config
import telebot


bot = telebot.TeleBot(config['bot_access_token'])

