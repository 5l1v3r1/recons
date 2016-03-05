import subprocess
import shlex
import os
# from plumbum import local


def chdir(bot, update):
    if len(shlex.split(update.message.text)) == 1:
        os.chdir(os.path.expanduser('~'))
    else:
        os.chdir(shlex.split(update.message.text)[1])
    bot.sendMessage(update.message.chat_id, os.path.abspath('.'))

functions = {
    'cd': chdir
}

def start(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat_id,
        text='logged into your server.')

def run_command(args):
    proc = subprocess.Popen(args, timeout)

def alpha(bot, update):
    try:
        print (os.path.abspath('.') + ' $', update.message.text)
        args = shlex.split(update.message.text)
        if args[0] in functions:
            functions[args[0]](bot, update)
        else:
            output = run_command(args)
            bot.sendMessage(update.message.chat_id, output)
    except Exception as e:
        bot.sendMessage(update.message.chat_id, 'ERROR: ' + str(e))
