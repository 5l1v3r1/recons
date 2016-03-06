from telegram import Updater
from settings import config
from commands import alpha, start

updater = Updater(token=config['bot_access_token'])
dispatcher = updater.dispatcher
dispatcher.addTelegramMessageHandler(alpha)
dispatcher.addTelegramCommandHandler('start', start)
