import subprocess
import shlex
import os
import threading
from contextlib import closing
import psutil
import telegram
import requests
from settings import config
from terminalapp import runcmd
import traceback
import sys


bot = telegram.Bot(token=config['bot_access_token'])

def chdir(chat_id, cmd):
    if len(shlex.split(cmd)) == 1:
        os.chdir(os.path.expanduser('~'))
    else:
        os.chdir(shlex.split(cmd)[1])
    bot.sendMessage(chat_id, os.path.abspath('.'))

button = [['0']]

def updatebutton(chat_id, cs, s):
    if s == 0:
        button[0][0] = '%s / - / -%%' % (cs, )
    else:
        button[0][0] = '%s / %s / %s%%' % (cs, s, int(cs * 100 / s))
    bot.sendChatAction(chat_id=chat_id, action=button[0][0])
    # bot.sendMessage(chat_id=chat_id, text='', reply_markup=telegram.ReplyKeyboardMarkup(button))


def wget(chat_id, cmd):
    try:
        argv = shlex.split(cmd)
        for url in argv[1:]:
            with closing(requests.get(url, stream=True)) as resp, open(url.split('/')[-1], 'wb') as out:
                for chunk in resp.iter_content(100 * 1024):
                    out.write(chunk)
                    updatebutton(chat_id, out.tell(), int(resp.headers.get('content-length', '0')))
            bot.sendMessage(chat_id=chat_id, text=url.split('/')[-1] + ' downloaded')
    except Exception as e:
        try:
            exc_info = sys.exc_info()
        finally:
            traceback.print_exception(*exc_info)
            del exc_info
        print(e)
        bot.sendMessage(chat_id=chat_id, text='ERROR: ' + str(e))



def kill_all_children(chat_id, cmd):
    proc_pid = int(shlex.split(cmd)[1])
    proc = psutil.Process(proc_pid)
    for child in proc.children(recursive=True):
        cpid = child.pid
        child.kill()
        bot.sendMessage(chat_id, '%s killed' % cpid)
    proc.kill()
    bot.sendMessage(chat_id, '%s killed' % proc_pid)


functions = {
    'cd': chdir,
    'killchi': kill_all_children,
    # 'wget': wget
}

def run(chat_id, cmd):
    prog = shlex.split(cmd)[0]
    if prog in functions:
        functions[prog](chat_id, cmd)
    else:
        threading.Thread(target=runcmd, args=(chat_id, cmd)).start()
