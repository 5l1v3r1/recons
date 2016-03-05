import os
from backend import run
import sys
import traceback
from settings import config


def start(bot, update):
    username = update.message.from_user.username
    chat_id = update.message.chat_id
    if username in config['admins']:
        config['admins'][username] = chat_id
        bot.sendMessage(
            chat_id=chat_id,
            text='admin recognized, access granted to the server')
    else:
        bot.sendMessage(
            chat_id=chat_id,
            text='unrecognized user, interrupting the security breach')


def alpha(bot, update):
    username = update.message.from_user.username
    chat_id = update.message.chat_id
    if username not in config['admins']:
        bot.sendMessage(
            chat_id=chat_id,
            text='unrecognized user, interrupting the security breach')
        return
    config['admins'][username] = chat_id
    try:
        print(os.path.abspath('.') + ' $', update.message.text)
        run(update.message.chat_id, update.message.text)
    except Exception as e:
        try:
            exc_info = sys.exc_info()
        finally:
            traceback.print_exception(*exc_info)
            del exc_info
        print(e)
        bot.sendMessage(update.message.chat_id, 'ERROR: ' + str(e))
